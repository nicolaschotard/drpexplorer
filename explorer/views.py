from django.http import HttpResponse
from explorer import explorer as Explorer


def explorer(request):
    """Data processing expolrer."""
    content = Explorer.explorer(request)
    return HttpResponse(content)