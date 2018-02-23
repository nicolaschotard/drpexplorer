from glob import glob
from django.conf import settings
from MarkupPy import markup

def init_page():
    staticpath = settings.STATIC_URL
    
    #head = '<link type="image/x-icon" rel="shortcut icon" href="static/js9/favicon.ico">'
    head = '<link type="image/x-icon" rel="shortcut icon" href="./favicon.ico">'
    footer = '%s - %s' % ("LSST Data Release Processing explorer",
                          settings.ADMIN[1])
    footer = "<div align='right'><font size='2'>%s</font><?div>" % footer
    # flot library
    script = [staticpath + 'flot/' + p.split('/')[-1]
              for p in glob(settings.STATICFILES_DIRS[0] + '/flot/*.min.js')]

    # jquery library
    script.extend([staticpath + 'jquery/jquery-3.3.1.min.js',
                   staticpath + 'jquery/ui/jquery-ui-1.12.1/jquery-ui.min.js',
                  ]
                 )

    # lsst JS scripts
    script.extend([staticpath + 'lsst/explorer.js'])
    
    # CSSs
    #theme = 'base'
    #theme = 'redmond'
    theme = 'start'
    themes = staticpath + 'jquery/ui/jquery-ui-themes-1.12.1/themes'
    css = (staticpath + 'lsst/css_hacks.css',
           themes + '/%s/jquery-ui.min.css' % theme,
           staticpath + 'jquery/ui/css/multi-select.css',
           staticpath + 'jquery/ui/css/jquery.ui.selectmenu.css'
          )

    # Web page intitialization
    page = markup.page()
    page.init(charset='utf-8',
              title='DRP explorer',
              footer=footer,
              script=script,
              css=css
              )
    page.addheader(head)
    return page
