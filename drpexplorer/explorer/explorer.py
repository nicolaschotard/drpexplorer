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
    page.addcontent("<h3>General info on the current DRP</h3>")
    page.addcontent("<h4>Paths to the repositories</h4>")
    page.addcontent("<p> - <b>Input</b>: %s</p>" % BUTLER.repo_input)
    page.addcontent("<p> - <b>Output</b>: %s</p>" % BUTLER.repo_output)
    
    # Info on the mapper, camera, package
    page.addcontent("<h4>Mapper info<h4>")
    page.addcontent("<p> - <b>Package</b>: %s" % BUTLER.mapper_package)
    page.addcontent("<p> - <b>Camera</b>: %s" % BUTLER.mapper_camera)
    page.addcontent("<p> - <b>Name</b>: %s" % BUTLER.mapper_name)
    
    # Other info, filter, skymap, etc.
    page.addcontent("<h4>Other info</h4>")
    page.addcontent("<p> - <b>Filters</b>: %s</p>" % ", ".join(BUTLER.filters))
    if hasattr(BUTLER, 'skymap'):
        page.addcontent("<p> - <b>Sky map</b>: %s</p>" % str(BUTLER.skymap_name))
    
    return page


def make_list(key, header, items, style='', onclick=''):  # width=180):
    html = "<div class='column'>"
    html += "<label for='list_%s'>%s</label>" % (key, header)
    html += "<select name='list_%s' id='visits_%s' style='%s'>" % (key, key, style)
    if len(items):
        html += "<option disabled selected>Please pick one</option>"
    else:
        html += "<option disabled selected>This list is empty</option>"
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
    dataids = [dataid for dataid in BUTLER.dataIds['raw'] if visit == str(dataid['visit'])]
    myimage = BUTLER.get_file('raw', dataids[0])[0]
    html = open(os.path.join(settings.BASE_DIR, "drpexplorer/explorer/js9_viewer.txt"), "r").read()
    html = html.replace("MYIMAGE", myimage)
    return html
    #html = "<br/>Selected visit: %s" % visit
    #html += "Raw data file: %s" % myimage
    #return html


def configs():
    """Configs info."""
    page = markup.page()
    style = "width=300px;"
    onclick = '"getconfiginfo(theitem)"'
    page.addcontent("<h3>Scripts configurations</h3> Click on a configuration to get more info.<p>")
    page.addcontent(make_list("config", "", BUTLER.configs, style=style, onclick=onclick))
    page.addcontent('<div style="clear:left" id="ConfigInfoDiv"></div>')
    return page


def schema():
    """Schemas info."""
    page = markup.page()
    style = "width=300px;"
    onclick = '"getschemainfo(theitem)"'
    page.addcontent("<h3>Catalogs schema</h3> Click on a schema to get more info.<p>")
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
    basename = "drpexplorer/explorer/static/links/%s" % os.path.basename(filename)
    # Does it have an extension?  [1]
    baseext = basename.split('[')
    if len(baseext) > 1:
        basename = baseext[0]
        extension = '[' + baseext[1]
    else:
        extension = ''
    if not os.path.exists(basename):
        os.symlink(filename, basename)
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
