from django.http import HttpResponse
from dre import dre as dremod
from dre import utils
from django.conf import settings


def main(request):
    """Main page."""
    page = utils.init_page()
    content = open(settings.BASE_DIR + "/dre/MAIN.txt", 'r').read()
    page.addcontent(content)
    return HttpResponse(page)


def dataproc(request):
    """Data processing expolrer."""
    content = dremod.dre(request)
    #page = utils.init_page()
    #header = '\n'.join(page.header).replace('black;">Processing', 'grey;">Processing')
    #content.header = header.split("\n")
    return HttpResponse(content)


def catexp(request):
    """Catalogs explorer."""
    content = dremod.dre(request)
    page = utils.init_page()
    header = '\n'.join(page.header).replace('black;">Catalogs', 'grey;">Catalogs')
    content.header = header.split("\n")
    return HttpResponse(content)


def imexp(request):
    """Images explorer."""
    content = dremod.dre(request)
    page = utils.init_page()
    header = '\n'.join(page.header).replace('black;">Images', 'grey;">Images')
    content.header = header.split("\n")
    return HttpResponse(content)


def doc(request):
    """Help and documenation."""
    page = utils.init_page()
    print('\n'.join(page.header))
    header = '\n'.join(page.header).replace('black;">Documentation', 'grey;">Documentation')
    page.header = header.split("\n")
    return HttpResponse(page)


