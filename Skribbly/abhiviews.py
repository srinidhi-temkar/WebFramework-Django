from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import forms 
from .forms import CreateUserForm,SearchForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import User,ComicStrip
from django.db.models import Q
from django.contrib.auth.decorators import login_required
login_required(login_url='login')

def home(request):
	return render(request,'webframeworks/home.html')
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
			messages.info(request, 'Username OR password is incorrect')
	context={}
	return render(request,'webframeworks/login.html')
def logoutUser(request):
	logout(request)
	return redirect('home')
@login_required(login_url='login')
def profile(request):
	return render(request,'webframeworks/profile.html')
def register(request):
	form = CreateUserForm()
	if request.method =="POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user )
			return redirect('login')
	context = {'form':form}
	return render(request,'webframeworks/register.html',context)
def gallery(request):
	return render(request,'webframeworks/gallery.html')
def tutorial(request):
	return render(request,'webframeworks/tutorial.html')
@login_required(login_url='login')
def mywork(request):
	return render(request,'webframeworks/mywork.html')

def comicsearch(request):
	ComicStrips=ComicStrip.objects.all()
	if(request.method=="POST"):
		form1=SearchForm(request.POST)
		if(form1.is_valid()):
			ComicStrips=ComicStrip.objects.filter(Q(title=request.POST.get('title','')))
			return render(request,"webframeworks/comicsearch.html",{'form1':form1,'ComicStrips':ComicStrips})
	else:
		form1=SearchForm()
		return render (request,"webframeworks/comicsearch.html",{'form1':form1,'ComicStrips':ComicStrips})