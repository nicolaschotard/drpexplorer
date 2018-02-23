from django.http import HttpResponse
from drpexplorer.explorer import explorer as Explorer


def explorer(request):
    """Data processing explorer."""
    content = Explorer.explorer()
    return HttpResponse(content)


def js9preload(request, filename=None):
    """Preload an image in JS9."""
    content = Explorer.js9preload(filename=filename)
    return HttpResponse(content)