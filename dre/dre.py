import os
from django.http import HttpResponse
from django.conf import settings
from MarkupPy import markup
from dre import utils


def overview():
    """ Overview info and plots"""
    overview = markup.page()
    msg1 = 'LSST Data Release Explorer'
    overview.span(msg1, style='float:left; font-size:100%;')
    return overview

    
def summary(hists):
    """Summary plots

    :param hists: 

    """
    summary = markup.page()
    summary.div(markup.oneliner.button('Unstack histograms', id='stack'))
    for h in hists:
        summary.div(style='float:left; margin-left:5px; margin-right:5px; margin-bottom:5px;' + h[2])
        summary.h3(h[0])
        summary.div(id=h[1], style='height:300px;')
        summary.div.close()
        summary.div.close()
        return summary

def js9():
    head = """<head>
    <link rel="import" href="dre/static/js9/js9.html">
    </head>
    """
    print(settings.BASE_DIR)
    html = open(os.path.join(settings.BASE_DIR, "dre/static/js9/js9.html"), 'r')
    content = html.read()
    html.close()
    content = content.replace('src="', 'src="file://%s/dre/static/js9/' % settings.BASE_DIR)
    content = content.replace('href="', 'href="file://%s/dre/static/js9/' % settings.BASE_DIR)
    print(content)
    return head

    
def help():

    f = open(os.path.join(settings.BASE_DIR, 'dre/static/help.txt'))
    help = f.read()
    f.close()
    return help

def dre(request, **kwargs):
    """DRE main

    :param request:
    :param **kwargs:

    """
    page = utils.init_page()
    
    hists = (('Redshift', 'z_hist', ''),
             ('MW E(B-V)', 'mwebv_hist', ''),
             ('Airmass', 'airmass_hist', ''),
             ('Phase (1st observation)', 'phase_hist', 'clear:left;'),
             ('Phase (all spectra)', 'specphase_hist', ''),
             ('# of epochs', 'nepoch_hist', ''),
             ('BSNf', 'B_hist', 'clear:left;'),
             ('VSNf', 'V_hist', ''), ('RSNf', 'R_hist', ''),
             ('SALT2 X1', 'X1_hist', 'clear:left;'),
             ('SALT2 color', 'color_hist', ''))


    # tabs
    possibletabs = {'overview': ['Overview', overview().__str__()],
                    'js9': ['js9', js9().__str__()],
                    'help': ['Help!', help()]
                    }

    default = ['overview', 'js9', 'help']
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
