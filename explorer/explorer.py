import os
from django.conf import settings
from MarkupPy import markup
from explorer import utils
from butler import processing


BUTLER = processing.Butler()


def home():
    """General info."""
    overview = markup.page()
    msg1 = 'LSST Data Release Explorer'
    overview.span(msg1, style='float:left; font-size:100%;')
    return overview


def drp():
    """Overview of the current DRP content."""
    drp = markup.page()
    drp.addcontent("<h2>General info on the current DRP</h2>")
    drp.addcontent("<h3>Paths to the repositories</h3>")
    drp.addcontent("<p> - <b>Input</b>: %s</p>" % BUTLER.repo_input)
    drp.addcontent("<p> - <b>Output</b>: %s</p>" % BUTLER.repo_output) 
    drp.addcontent("<h3>Mapper info</h3>")
    drp.addcontent("<p> - <b>Package</b>: %s" % BUTLER.mapper_package)
    drp.addcontent("<p> - <b>Camera</b>: %s" % BUTLER.mapper_camera)
    drp.addcontent("<p> - <b>Name</b>: %s" % BUTLER.mapper_name)
    drp.addcontent("<h3>Other info</h3>")
    drp.addcontent("<p> - <b>Filters</b>: %s</p>" % ", ".join(BUTLER.filters))
    drp.addcontent("<p> - <b>Sky map name</b>: %s</p>" % str(BUTLER.skymap_name))
    #drp.addcontent(str(BUTLER.skymap_doc))
    return drp


def visits():
    """List of visits."""
    visits = markup.page()
    visits.addcontent(str(BUTLER.visits['g'][0]))
    visits.addcontent(str(len(BUTLER.visits['g'])))
    return visits
    

def default_page():
    """ Default output"""
    page = markup.page()
    msg1 = 'LSST Data Release Explorer default page'
    page.span(msg1, style='float:left; font-size:100%;')
    return page


def js9():
    head = """<head>
    <link rel="import" href="explorer/static/js9/js9.html">
    </head>
    """
    print(settings.BASE_DIR)
    html = open(os.path.join(settings.BASE_DIR, "explorer/static/js9/js9.html"), 'r')
    content = html.read()
    html.close()
    content = content.replace('src="', 'src="file://%s/explorer/static/js9/' % \
                              settings.BASE_DIR)
    content = content.replace('href="', 'href="file://%s/explorer/static/js9/' % \
                              settings.BASE_DIR)
    print(content)
    return head


def help():

    f = open(os.path.join(settings.BASE_DIR, 'explorer/static/help.txt'))
    help = f.read()
    f.close()
    return help


def explorer(request, **kwargs):
    """DRP explorer main.

    :param request:
    :param **kwargs:
    """
    # Initialize html page
    page = utils.init_page()

    # tabs
    possibletabs = {#'home': ['Home', home().__str__()],
                    'drp': ['DRP', drp().__str__()],
                    'visits': ['Visits', visits().__str__()],
                    'skymap': ['Sky Map', default_page().__str__()],
                    'astrometry': ['Astrometry', default_page().__str__()],
                    'photometry': ['Photometry', default_page().__str__()],
                    'refcat': ['Ref. Cat.', default_page().__str__()],
                    'images': ['Images', default_page().__str__()],
                    'catalogs': ['Catalogs', default_page().__str__()],
                    'historic': ['Historic', default_page().__str__()],
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
