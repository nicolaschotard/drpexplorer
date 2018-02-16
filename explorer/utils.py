from glob import glob
from django.conf import settings
from MarkupPy import markup

HEADER = open(settings.BASE_DIR + "/dre/HEADER.txt", 'r').read()

def init_page():
    footer = '<p> %s - %s' % ("LSST data release processing explorer",
                              settings.ADMIN[1])
    
    script = ['/static/flot/' + p.split('/')[-1]
              for p in glob(settings.STATICFILES_DIRS[0] + '/flot/*.min.js')]
    script.extend(['/static/jquery2/jquery-1.6.1.min.js',
                   '/static/jquery2/jquery.jsanalysis.js',
                   '/static/jquery2/ui/js/ui.min.js',
                   #'/static/jquery/jquery-3.3.1.min.js',
                   #'/static/jquery/ui/jquery-ui-1.12.1/jquery-ui.js',
                   '/static/jquery/jquery.konami.js']
              )
    script.extend(['/static/lsst/dre.js'])
    #print('toto', HEADER, 'toto')
    page = markup.page()
    page.init(charset='utf-8',
              title='Data Release Explorer',
              header=HEADER,
              footer='<font size="3">%s</font><p>' % footer,
              script=script,
              css=('/static/lsst/css_hacks.css',
                   '/static/jquery2/ui/css/smoothness/jquery-ui-1.8.9.custom.css',
                   '/static/jquery2/ui/css/jquery.multiselect.css',
                   '/static/jquery2/ui/css/jquery.ui.selectmenu.css'
                   #'/static/jquery/ui/jquery-ui-themes-1.12.1/themes/pepper-grinder/jquery-ui.min.css',
                   ##'/static/jquery/ui/css/jquery.multiselect.css',
                   #'/static/jquery/ui/css/multi-select.css',
                   #'/static/jquery/ui/css/jquery.ui.selectmenu.css'
               ))
    #page.addheader(HEADER)
    #print('toto', page.header, 'toto')
    return page