"""tesisweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
#from django.contrib.staticfiles.views import serve
from django.views.generic import RedirectView
from django.views.generic.base import TemplateView
from web.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('web.urls')),
    #re_path(r'^$', serve, kwargs={'path': '/static/index.html'}),
    re_path(r'^$', TemplateView.as_view(template_name="index.html"), name="home")
    #re_path(r'^(?!/?static/)(?!/?media/)(?P<path>.*)$',RedirectView.as_view(url='/static/%(path)s', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)