"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from . import views


urlpatterns = [
    path('', include('smarteye.urls')),
    # path('', views.homepage),
    # path('something/', views.test),
    # path('camera_test/', views.camera_test),
    # path('my_camera_test/', views.my_camera_test),
    path('admin/', admin.site.urls),
    # path('admin/', views.homepage),
    # path('test/', views.index, name='index'),
    # path('facecam_feed/', views.facecam_feed, name='facecam_feed'),



    #display both cameras
    # path('camera_test/', views.index, name='index'),

    #access the laptop camera
    # path('video_feed/', views.video_feed, name='video_feed'),

    #access the phone camera
    # path('webcam_feed/', views.webcam_feed, name='webcam_feed'),


    # path('facecam_feed', views.facecam_feed, name='facecam_feed'),
]
