from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import forms 
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Artist, ComicStrip, Comment

# Create your views here.
def home(request):
	return render(request,'Skribbly/index.html')
def index(request):
	return redirect('home')
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('profile')
		else:
			messages.info(request, 'Username OR Password is incorrect')
	context={}
	return render(request,'Skribbly/login.html')
def logoutUser(request):
	logout(request)
	return redirect('home')
def profile(request):
	return render(request,'Skribbly/profile.html')
def register(request):
	form = CreateUserForm()
	if request.method =="POST":
		form = CreateUserForm(request.POST)
		# print(form)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user )
			return redirect('login')
	context = {'form':form}
	return render(request,'Skribbly/register.html',context)
def gallery(request):
	return render(request,'Skribbly/gallery.html')
def tutorial(request):
	return render(request,'Skribbly/tutorial.html')
def mywork(request):
	return render(request,'Skribbly/mywork.html')