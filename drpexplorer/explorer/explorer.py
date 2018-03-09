import os
import numpy
from django.conf import settings
from MarkupPy import markup
from drpexplorer.explorer import utils
from drpexplorer.butler import processing


BUTLER = processing.Butler()


def home():
    """General info."""
    page = markup.page()
    page.span('Welcome to the LSST Data Release explorer', 
              style='float:left; font-size:100%;')
    return page


def square_list(items):
    html = '<ul style="list-style-type:square">'
    html += "".join(["<li>%s</li>" % item for item in items])
    html += '</ul>'
    return html
 

def drp():
    """Overview of the current DRP content."""
    page = markup.page()
    
    # General info on the data repository
    page.addcontent("<h2>General info on the current DRP</h2>")
    
    # Repos
    page.addcontent("<h3>Paths to the repositories</h3>")
    page.addcontent(square_list(["<b>Input</b>: %s</li>" % BUTLER.repo_input,
                                 "<b>Output</b>: %s</li>" % BUTLER.repo_output
                                ]
                               )
                   )

    # Info on the mapper, camera, package
    page.addcontent("<h3>Mapper info</h3>")
    page.addcontent(square_list(["<b>Package</b>: %s" % BUTLER.mapper_package,
                                 "<b>Camera</b>: %s" % BUTLER.mapper_camera,
                                 "<b>Name</b>: %s" % BUTLER.mapper_name
                                ]
                               )
                   )
        
    page.addcontent("<h3>Filters and visits</h3>")
    page.addcontent("<table>")
    page.addcontent("<tr><th>Name</th>")
    page.addcontent("".join(["<td>%s</td>" % filt for filt in BUTLER.filters]))
    page.addcontent("</tr>")
    page.addcontent("<tr><th>#Visits</th>")
    page.addcontent("".join(["<td>%i</td>" % len(BUTLER.visits[filt]) for filt in BUTLER.filters]))
    page.addcontent("</tr>")
    page.addcontent("</table>")
    
    # Other info, filter, skymap, etc.
    items = []
    if hasattr(BUTLER, 'skymap'):
        items.append("<b>Sky map</b>: %s" % str(BUTLER.skymap_name))
    if len(items):
        page.addcontent("<h3>Other info</h3>")
        page.addcontent(square_list(items))

    return page


def make_list(key, header, items, style='', onclick=''):  # width=180):
    html = "<div class='column'>"
    html += "<label for='list_%s'>%s</label>" % (key, header)
    html += "<select name='list_%s' id='visits_%s' style='%s'>" % (key, key, style)
    if len(items):
        html += "<option selected>Please pick one</option>"
    else:
        html += "<option selected>This list is empty</option>"
    for item in sorted(items):
        oc = onclick.replace('theitem', "'%s'" % str(item))
        html += "<option value=%s onclick=%s>%s</option>" % (item, oc, item)
    html += "</select>"
    html += "</div>"
    return html
    
def visits():
    """List of visits."""
    page = markup.page()
    style = 'width:180px;'
    onclick = '"getvisitinfo(theitem)"'
    page.addcontent("<h3>List of all visits for all filter</h3> Click on one visit to get more info.<p>")
    for filt in sorted(BUTLER.visits):
        header = "%i visits for <b>%s</b> filter" % (len(BUTLER.visits[filt]), filt)
        page.addcontent(make_list(filt, header, BUTLER.visits[filt], style=style, onclick=onclick))
    page.addcontent("""<div style="clear:left" id="VisitInfoDiv"></div>""")
    return page


def get_visit_info(visit):
    
    # Get file and show them as lists
    datatypes = ['raw', 'calexp']
    dataids = [dataid for dataid in BUTLER.dataIds['raw'] if visit == str(dataid['visit'])]
    html = "<br/><p><b>Selected visit: %s</b></p>" % visit

    for datatype in datatypes:
        images = list(set(numpy.concatenate([BUTLER.get_file(datatype, dataid) for dataid in dataids])))

        # Nice list
        key, header, style = datatype, '%s data files (%i)' % (datatype.title(), len(images)), 'width:350px;'
        html += "<div class='column'>"
        html += "<label for='list_%s'>%s</label>" % (key, header)
        html += "<select name='list_%s' id='visits_%s' style='%s'>" % (key, key, style)
        if len(images):
            html += "<option disabled selected>Please pick one</option>"
        else:
            html += "<option disabled selected>This list is empty</option>"
        for image in sorted(images):
            onclick = "window.open('js9preload/%s', 'newwindow', 'width=800,height=800'); return false;" % image #(image, image)
            if datatype == 'raw':
                html += '<option value=%s onclick="%s">%s</option>' % (image, onclick, os.path.basename(image))
            else:
                html += '<option value=%s onclick="%s">%s</option>' % (image, onclick, image.replace(BUTLER.repo_output, ''))
        html += "</select>"
        html += "</div>"
    
    return html


def configs():
    """Configs info."""
    page = markup.page()
    style = "width=300px;"
    onclick = '"getconfiginfo(theitem)"'
    page.addcontent("<h2>Scripts configurations</h2> Click on a configuration to get more info.<p>")
    page.addcontent(make_list("config", "", BUTLER.configs, style=style, onclick=onclick))
    page.addcontent('<div style="clear:left" id="ConfigInfoDiv"></div>')
    return page


def schema():
    """Schemas info."""
    page = markup.page()
    style = "width=300px;"
    onclick = '"getschemainfo(theitem)"'
    page.addcontent("<h2>Catalogs schema</h2> Click on a schema to get more info.<p>")
    page.addcontent(make_list("schema", "", BUTLER.schemas, style=style, onclick=onclick))
    page.addcontent('<div style="clear:left" id="SchemaInfoDiv"></div>')
    return page


def get_schema(schema):
    if schema not in BUTLER.schemas:
        page = markup.page()
        page.addcontent("ERROR: No data found for <b>%s</b>. Possible schemas are:<p>" % schema)
        page.addcontent("<ul>%s</ul>" % "".join(["<li>%s</li>" % sch for sch in BUTLER.schemas]))
        return page
    else:
        return make_menu_from_dict(BUTLER.schemas[schema])
    

def get_config(config):
    if config not in BUTLER.configs:
        page = markup.page()
        page.addcontent("ERROR: No data found for <b>%s</b>. Possible configs are:<p>" % config)
        page.addcontent("<ul>%s</ul>" % "".join(["<li>%s</li>" % cfg for cfg in BUTLER.configs]))
        return page
    else:
        return make_menu_from_dict(BUTLER.configs[config])
    
    
def make_menu_from_dict(dic):
    html = "<ul>"
    for key in sorted(list(dic.keys())):
        if isinstance(dic[key], dict):
            html += "<li> %s" % key
            html += make_menu_from_dict(dic[key])
            html += "</li>"
        elif isinstance(dic[key], list):
            html += "<li>%s: [%s]</li>" % (key, ",".join(str(v) for v in dic[key]))
        else:
            html += "<li>%s: %s</li>" % (key, str(dic[key]))
    html += "</ul>"
    return html
    

def default_page():
    """ Default output"""
    page = markup.page()
    msg1 = 'LSST Data Release Explorer default page'
    page.span(msg1, style='float:left; font-size:100%;')
    return page


def js9preload(filename=None):
    """Pre-load (or load) an image in JS9."""
    msg = "For multi-extensions files, go to 'View -> Extensions' to select the extension to display."
    
    basename = make_link(filename)
        
    # Get the content of the JS9 window
    page = open(os.path.join(settings.BASE_DIR, "drpexplorer/explorer/js9_content.txt"), "r").read()
    
    # Put this file name in the JS9 pre_load function
    page = page.replace("IMAGETOLOAD", "/" + basename) #"links/%s" % image_name)
    page = page.replace("INFO", msg)
    return page


def make_link(filename=None):
    if filename is None:
        return None
    
    # Make sure the directory containing the symbolic links exists
    if not os.path.isdir("drpexplorer/explorer/static/links/"):
        os.mkdir("drpexplorer/explorer/static/links/")
    
    # Name of the file to load, and create a link if it does not exist yet
    file_path = os.path.dirname(filename)
    file_name = os.path.basename(filename)
    
    # Does it have an extension?  [1]
    baseext = file_name.split('[')
    if len(baseext) > 1:
        file_name = baseext[0]
        extension = '[' + baseext[1]
    else:
        extension = ''
        
    # Base name to create the link at the proper place
    basename = "drpexplorer/explorer/static/links/%s" % file_name
    
    # Create the link without the extension
    if os.path.islink(basename):
        os.remove(basename)
    os.symlink(os.path.join(file_path, file_name), basename)
    
    # Return the base name plus the extension
    return basename+extension


def images():
    myimage = "/sps/lsst/data/clusters/workflow/weeklies/work/201749004/02-singleFrameDriver/pardir/output/calexp/08BO01/SCL-2241_P2/2008-09-04/r/bkgd-1022360-22.fits"
    html = open(os.path.join(settings.BASE_DIR, "drpexplorer/explorer/js9_viewer.txt"), "r").read()
    html = html.replace("MYIMAGE", myimage)
    return html


def js9():
    msg = "<h3>JS9 window utility (<a href=https://js9.si.edu/ target='_blanck'>website</a>, <a href=https://github.com/ericmandel/js9 target='_blanck'>github</a>)</h3>"
    msg += "<p>Use <b>File -> open local file...</b> to load a local file, or the following input box for a file on the server.</p>"
    msg += "<input type='text' id='filetoload' value='Absolute path of a file located on the running server.' style='width: 500px'> "
    msg += "<button onclick='loadmyfile()'>Load me</button>"    
    lines = open(os.path.join(settings.BASE_DIR, "drpexplorer/explorer/js9_content.txt"), "r").readlines()
    page = "".join([(line if not '<body' in line else '<body>') for line in lines])
    page = page.replace("INFO", msg)
    return page


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
                    #'skymap': ['Sky Map', default_page().__str__()],
                    #'astrometry': ['Astrometry', default_page().__str__()],
                    #'photometry': ['Photometry', default_page().__str__()],
                    #'refcat': ['Ref. Cat.', default_page().__str__()],
                    #'images': ['Images', images().__str__()],
                    #'catalogs': ['Catalogs', default_page().__str__()],
                    #'historic': ['Historic', default_page().__str__()],
                    'configs': ['Configs', configs().__str__()],
                    'schema': ['Schema', schema().__str__()],
                    'js9': ['JS9', js9().__str__()],
                    #'help': ['Help!', help()]
                   }

    default = list(possibletabs.keys())
    tabs = [['#'+t] + possibletabs[t] for t in default if t in possibletabs]

    page.div(id='tabs')
    # list of tabs
    page.ul(markup.oneliner.li([markup.oneliner.a(t[1], href=t[0], tab=True)
                                for t in tabs]))

    # and corresponding content divs
    for t in tabs:
        page.div(t[2], id=t[0].replace('#', ''), style="height: 89%; overflow-y: auto;")
    page.div.close()

    return page
