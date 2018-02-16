import os
from django.http import HttpResponse
from django.conf import settings
from MarkupPy import markup
from explorer import utils


def home():
    """ Overview info and plots"""
    overview = markup.page()
    msg1 = 'LSST Data Release Explorer'
    overview.span(msg1, style='float:left; font-size:100%;')
    return overview

    
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
    content = content.replace('src="', 'src="file://%s/explorer/static/js9/' % settings.BASE_DIR)
    content = content.replace('href="', 'href="file://%s/explorer/static/js9/' % settings.BASE_DIR)
    print(content)
    return head

    
def help():

    f = open(os.path.join(settings.BASE_DIR, 'explorer/static/help.txt'))
    help = f.read()
    f.close()
    return help

def explorer(request, **kwargs):
    """DRE main

    :param request:
    :param **kwargs:

    """
    page = utils.init_page()
    
    # tabs
    possibletabs = {'home': ['Home', home().__str__()],
                    'drp': ['DRP', default_page().__str__()],
                    'visits': ['Visits', default_page().__str__()],
                    'skymap': ['Sky Map', default_page().__str__()],
                    'astrometry': ['Astrometry', default_page().__str__()],
                    'photometry': ['Photometry', default_page().__str__()],
                    'images': ['Images', default_page().__str__()],
                    'catalogs': ['Catalogs', default_page().__str__()],
                    'help': ['Help!', help()]
                    }

    default = list(possibletabs.keys())
    tabs = [['#'+t] + possibletabs[t] for t in default if t in possibletabs]

    page.div(id='tabs', lctarget=kwargs.get('lctarget'))
    # list of tabs
    page.ul(markup.oneliner.li([markup.oneliner.a(t[1], href=t[0], tab=True) for t in tabs]))
    # and corresponding content divs
    for t in tabs:
        page.div(t[2], id=t[0].replace('#', ''))
    page.div.close()
    return page
    #return HttpResponse(page.__str__())
