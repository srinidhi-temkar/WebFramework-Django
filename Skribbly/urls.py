
from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from . import views
from .views import *

urlpatterns = [
    path('',views.home,name='home'),
	path('login/',views.loginPage,name='login'),
	path('logout/',views.logoutUser,name='logout'),
	path('register/',views.register,name='register'),
	path('profile/<user>/',views.profile,name='profile'),
	path('gallery/',views.gallery,name='gallery'),
	path('gallery_search/',views.gallery,name='gallery_search'),
	path('canvas/',views.canvas,name='canvas'),
	path('tutorial/',views.tutorial,name='tutorial'),
	path('index/',views.index,name='index'),
	path('edit_profile/',views.edit_profile,name='edit_profile'),
	path('comicpage/<int:pk>/<title>/',views.comicpage,name='comicpage'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)