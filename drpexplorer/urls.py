"""drpexplorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from drpexplorer.explorer import views, explorer


# Main url patterns
urlpatterns = [path('admin/', admin.site.urls),                  # admin
               path('', views.explorer, name='DRP explorer')]   # explorer

# JS9 related urls
urlpatterns += [path('js9preload/', views.js9preload),
                path('js9preload/<path:filename>', views.js9preload),
                path('makelink/<path:filename>', views.makelink)
               ]

# Schemas and configurations
urlpatterns += [path('schema/', views.getschema),
                path('config/', views.getconfig),
                path('schema/<str:schema>', views.getschema),
                path('config/<str:config>', views.getconfig)
               ]

# Visit info
urlpatterns += [path('visit/', views.getvisitinfo),
                path('visit/<str:visit>', views.getvisitinfo)]
