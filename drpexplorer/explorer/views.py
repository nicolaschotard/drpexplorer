from django.http import HttpResponse
from drpexplorer.explorer import explorer as Explorer
import json

def explorer(request):
    """Data processing explorer."""
    content = Explorer.explorer()
    return HttpResponse(content)


def js9preload(request, filename=None):
    """Preload an image in JS9."""
    content = Explorer.js9preload(filename=filename)
    return HttpResponse(content)

def makelink(request, filename=None):
    link = Explorer.make_link(filename=filename)
    return HttpResponse(json.dumps({'link': link}), content_type='application/json')