import os
from django.conf import settings
from MarkupPy import markup
from drpexplorer.explorer import utils
from drpexplorer.butler import processing


BUTLER = processing.Butler()


def home():
    """General info."""
    overview = markup.page()
    msg1 = 'Welcome to the LSST Data Release explorer'
    overview.span(msg1, style='float:left; font-size:100%;')
    return overview


def drp():
    """Overview of the current DRP content."""
    drp = markup.page()
    
    # General info on the data repository
    drp.addcontent("<h2>General info on the current DRP</h2>")
    drp.addcontent("<h3>Paths to the repositories</h3>")
    drp.addcontent("<p> - <b>Input</b>: %s</p>" % BUTLER.repo_input)
    drp.addcontent("<p> - <b>Output</b>: %s</p>" % BUTLER.repo_output)
    
    # Info on the mapper, camera, package
    drp.addcontent("<h3>Mapper info</h3>")
    drp.addcontent("<p> - <b>Package</b>: %s" % BUTLER.mapper_package)
    drp.addcontent("<p> - <b>Camera</b>: %s" % BUTLER.mapper_camera)
    drp.addcontent("<p> - <b>Name</b>: %s" % BUTLER.mapper_name)
    
    # Other info, filter, skymap, etc.
    drp.addcontent("<h3>Other info</h3>")
    drp.addcontent("<p> - <b>Filters</b>: %s</p>" % ", ".join(BUTLER.filters))
    drp.addcontent("<p> - <b>Sky map</b>: %s</p>" % str(BUTLER.skymap_name))
    
    return drp


def visits():
    """List of visits."""
    visits = markup.page()
    visits.css(("nav ul{height:200px; width:18%;}",
                "nav ul{overflow:hidden; overflow-y:scroll;}"
               )
              )
    def make_list(header, items):
        html = "<header>%s</header>" % header
        html += "<nav><ul>"
        for item in items:
            html += "<li>%s</li>" % item
        html += "</ul></nav>"
        return html
    
    for filt in BUTLER.visits:
        visits.addcontent(make_list(filt, BUTLER.visits[filt]))
        
    return visits


def configs():
    """Overview of the current DRP content."""
    configs = markup.page()
    
    # General info on the data repository
    configs.addcontent("<h3>Paths to the repositories</h3>")
    configs.select(id='select_config', multiple='multiple')
    for subset in subsets:
        configs.optgroup(ol.option([t.name for t in tgts],
                                    value=[t.id for t in tgts]),
                          label=subset.capitalize())
    quantity.select.close()

    drp.addcontent("<p> - <b>Input</b>: %s</p>" % BUTLER.repo_input)    
    return drp


def schema():
    """Overview of the current DRP content."""
    drp = markup.page()
    
    # General info on the data repository
    drp.addcontent("<h3>Paths to the repositories</h3>")
    drp.addcontent("<p> - <b>Input</b>: %s</p>" % BUTLER.repo_input)    
    return drp
    

def default_page():
    """ Default output"""
    page = markup.page()
    msg1 = 'LSST Data Release Explorer default page'
    page.span(msg1, style='float:left; font-size:100%;')
    return page


def js9preload(filename=None):
    """Pre-load (or load) an image in JS9."""
    # Make sure the directory containing the symbolic links exists
    if not os.path.isdir("drpexplorer/explorer/static/links/"):
        os.mkdir("drpexplorer/explorer/static/links/")
    
    # Get the content of the JS9 window
    js9 = open(os.path.join(settings.BASE_DIR, "drpexplorer/explorer/js9_content.txt"), "r").read()
    
    # Name of the file to load, and create a link if it does not exist yet
    basename = "drpexplorer/explorer/static/links/%s" % os.path.basename(filename)
    if not os.path.exists(basename):
        os.symlink(filename, basename)
    
    # Put this file name in the JS9 pre_load function
    js9 = js9.replace("IMAGETOLOAD", "/" + basename) #"links/%s" % image_name)
    
    return js9


def images():
    html = open(os.path.join(settings.BASE_DIR, "drpexplorer/explorer/js9_viewer.txt"), "r").read()
    html = html.replace("JS9CONTENT", "toto")
    return html


def js9():
    msg = "This JS9 window will use the browser's ability to read <b>local</b> files only"
    lines = open(os.path.join(settings.BASE_DIR, "drpexplorer/explorer/js9_content.txt"), "r").readlines()
    js9 = "".join([(line if not '<body' in line else '<body>') for line in lines])
    js9 = js9.replace("INFO", msg)
    return js9


def help():

    f = open(os.path.join(settings.BASE_DIR, 'drpexplorer/explorer/static/help.txt'))
    help = f.read()
    f.close()
    return help


def explorer():
    """DRP explorer main."""
    # Initialize html page
    page = utils.init_page()

    # tabs
    possibletabs = {'home': ['Home', home().__str__()],
                    'drp': ['DRP', drp().__str__()],
                    'visits': ['Visits', visits().__str__()],
                    'skymap': ['Sky Map', default_page().__str__()],
                    'astrometry': ['Astrometry', default_page().__str__()],
                    'photometry': ['Photometry', default_page().__str__()],
                    'refcat': ['Ref. Cat.', default_page().__str__()],
                    'images': ['Images', images().__str__()],
                    'catalogs': ['Catalogs', default_page().__str__()],
                    'historic': ['Historic', default_page().__str__()],
                    'configs': ['Configs', configs().__str__()],
                    'schema': ['Schema', schema().__str__()],
                    'js9': ['JS9', js9().__str__()],
                    'help': ['Help!', help()]
                   }

    default = list(possibletabs.keys())
    tabs = [['#'+t] + possibletabs[t] for t in default if t in possibletabs]

    page.div(id='tabs')
    # list of tabs
    page.ul(markup.oneliner.li([markup.oneliner.a(t[1], href=t[0], tab=True)
                                for t in tabs]))

    # and corresponding content divs
    for t in tabs:
        page.div(t[2], id=t[0].replace('#', ''))
    page.div.close()

    return page
