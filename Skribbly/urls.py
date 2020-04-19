from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='home'),
	path('login/',views.loginPage,name='login'),
	path('logout/',views.logoutUser,name='logout'),
	path('register/',views.register,name='register'),
	path('profile/',views.profile,name='profile'),
	path('gallery/',views.gallery,name='gallery'),
	path('mywork/',views.mywork,name='mywork'),
	path('tutorial/',views.tutorial,name='tutorial'),
	path('index/',views.index,name='index'),
]