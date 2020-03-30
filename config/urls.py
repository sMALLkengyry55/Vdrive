"""vdrive URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import re_path, include
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, re_path
from django.contrib import admin

# Remove default django '/' site_url to hide 'View Site' button in Admin header
admin.site.site_url = None

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^', include('apps.vdrive.urls', namespace='vdrive')),
    re_path(r'^accounts/', include('django.contrib.auth.urls')),
    re_path(r'^social/', include('social_django.urls', namespace='social')),
]
