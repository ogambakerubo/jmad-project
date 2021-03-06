"""jmad URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include

from rest_framework import routers

from solos import views
from albums.views import AlbumViewSet, TrackViewSet
from solos.views import SoloViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'albums', AlbumViewSet)
router.register(r'tracks', TrackViewSet)
router.register(r'solos', SoloViewSet)


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('', views.index),
    # Apps
    path('recordings/<slug:album>/<slug:track>/<slug:artist>/',
         views.solo_detail, name='solo_detail_view'),
    # API
    path('api/', include(router.urls))
]
