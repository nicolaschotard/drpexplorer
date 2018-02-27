import os
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


def drp():
    """Overview of the current DRP content."""
    page = markup.page()
    
    # General info on the data repository
    page.addcontent("<h2>General info on the current DRP</h2>")
    page.addcontent("<h3>Paths to the repositories</h3>")
    page.addcontent("<p> - <b>Input</b>: %s</p>" % BUTLER.repo_input)
    page.addcontent("<p> - <b>Output</b>: %s</p>" % BUTLER.repo_output)
    
    # Info on the mapper, camera, package
    page.addcontent("<h3>Mapper info</h3>")
    page.addcontent("<p> - <b>Package</b>: %s" % BUTLER.mapper_package)
    page.addcontent("<p> - <b>Camera</b>: %s" % BUTLER.mapper_camera)
    page.addcontent("<p> - <b>Name</b>: %s" % BUTLER.mapper_name)
    
    # Other info, filter, skymap, etc.
    page.addcontent("<h3>Other info</h3>")
    page.addcontent("<p> - <b>Filters</b>: %s</p>" % ", ".join(BUTLER.filters))
    page.addcontent("<p> - <b>Sky map</b>: %s</p>" % str(BUTLER.skymap_name))
    
    return page


def make_list(header, items):
    html = "<label for='visits_%s'>  %s  </label>" % (header, header)
    html += "<select name='visits_%s' id='visits_%s'>" % (header, header)
    for item in items:
        html += "<option value=%s>%s</option>" % (item, item)
    html += "</select>   "
    html += """<script>
    $( "#visits_%s" )
    .selectmenu()
    .selectmenu( "menuWidget" )
    .addClass( "overflow" );
    </script>""" % header
    return html
    
def visits():
    """List of visits."""
    page = markup.page()
    head = """<style>
    label { display: block; }
    select { width: 150px; }
    .overflow { height: 200px; }
    </style>
    """
    
    page.addcontent("List of all visits for all filter. Click on a visit to get more info.<p>")
    for filt in sorted(BUTLER.visits):
        page.addcontent(make_list(filt, BUTLER.visits[filt]))
    
    return page


def configs():
    """Configs info."""
    page = markup.page()
    head = """<style>
    label { display: block; }
    select { width: 150px; }
    .overflow { height: 200px; }
    </style>
    """
    page.addcontent("List of all scripts configuration. Click on a config to get more info: ")
    page.addcontent(make_list("", BUTLER.configs))
    
    return page


def schema():
    """Schemas info."""
    page = markup.page()
    head = """<style>
    label { display: block; }
    select { width: 150px; }
    .overflow { height: 200px; }
    </style>
    """
    page.addcontent("List of all scripts configuration. Click on a config to get more info: ")
    page.addcontent(make_list("", BUTLER.schemas))
    
    return page
    

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
    basename = "drpexplorer/explorer/static/links/%s" % os.path.basename(filename)
    if not os.path.exists(basename):
        os.symlink(filename, basename)
    return basename


def images():
    html = open(os.path.join(settings.BASE_DIR, "drpexplorer/explorer/js9_viewer.txt"), "r").read()
    html = html.replace("JS9CONTENT", "toto")
    return html


def js9():
    msg = "<h3>JS9 window utility (<a href=https://js9.si.edu/ target='_blanck'>website</a>, <a href=https://github.com/ericmandel/js9 target='_blanck'>github</a>)</h3>"
    msg += "<p>Use <b>'File -> open local file...</b>' to load local files, or the following input box for file on the server.</p>"
    msg += "<input type='text' id='filetoload' value='Absolute path to a file located on the running server' style='width: 500px'> "
    msg += "<button onclick='loadmyfile()'>Load me</button>"
    msg += """
    <script>
    function loadmyfile() {
        var myfile = document.getElementById("filetoload").value;
        $.getJSON(`/makelink/` + myfile, function (mylink) { JS9.Load(mylink['link'], {scale: 'log', zoom: 'to fit'}) });
    }
    </script>"""
    
    msg += ""
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
     
    possibletabs = {'home': ['<font color="red">Home</font>', home().__str__()],
                    'drp': ['<font color="green">DRP</font>', drp().__str__()],
                    'visits': ['<font color="orange">Visits</font>', visits().__str__()],
                    'skymap': ['<font color="red">Sky Map</font>', default_page().__str__()],
                    'astrometry': ['<font color="red">Astrometry</font>', default_page().__str__()],
                    'photometry': ['<font color="red">Photometry</font>', default_page().__str__()],
                    'refcat': ['<font color="red">Ref. Cat.</font>', default_page().__str__()],
                    'images': ['<font color="orange">Images</font>', images().__str__()],
                    'catalogs': ['<font color="red">Catalogs</font>', default_page().__str__()],
                    'historic': ['<font color="red">Historic</font>', default_page().__str__()],
                    'configs': ['<font color="orange">Configs</font>', configs().__str__()],
                    'schema': ['<font color="orange">Schema</font>', schema().__str__()],
                    'js9': ['<font color="green">JS9</font>', js9().__str__()],
                    'help': ['<font color="red">Help!</font>', help()]
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
