from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

urlpatterns = [
    path('',views.home,name='home'),
	path('login/',views.loginPage,name='login'),
	path('logout/',views.logoutUser,name='logout'),
	path('register/',views.register,name='register'),
	path('profile/<username>/',views.profile,name='profile'),
	path('gallery/',views.gallery,name='gallery'),
	path('canvas/',views.canvas,name='canvas'),
	path('tutorial/',views.tutorial,name='tutorial'),
	path('index/',views.index,name='index'),
	path('edit_profile/',views.edit_profile,name='edit_profile'),
	path('like/', views.like, name='like'),
	path('favorite/', views.favorite, name='favorite'),
]

