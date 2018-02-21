from glob import glob
from django.conf import settings
from MarkupPy import markup

def init_page():
    footer = '<p> %s - %s' % ("LSST Data Release Processing explorer",
                              settings.ADMIN[1])

    # flot library
    script = ['/static/flot/' + p.split('/')[-1]
              for p in glob(settings.STATICFILES_DIRS[0] + '/flot/*.min.js')]

    # jquery library
    script.extend(['/static/jquery/jquery-3.3.1.min.js',
                   '/static/jquery/ui/jquery-ui-1.12.1/jquery-ui.min.js',
                  ]
                 )

    # lsst JS scripts
    script.extend(['/static/lsst/explorer.js'])

    # CSSs
    #theme = 'base'
    #theme = 'redmond'
    theme = 'start'
    themes = '/static/jquery/ui/jquery-ui-themes-1.12.1/themes'
    css = (themes + '/%s/jquery-ui.min.css' % theme,
           '/static/jquery/ui/css/multi-select.css',
           '/static/jquery/ui/css/jquery.ui.selectmenu.css',
           '/static/lsst/css_hacks.css',
          )

    # Web page intitialization
    page = markup.page()
    page.init(charset='utf-8',
              title='DRP explorer',
              footer='<font size="2">%s</font><p>' % footer,
              script=script,
              css=css)
    return page
