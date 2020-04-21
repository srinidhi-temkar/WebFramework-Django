from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import forms 
from .forms import CreateUserForm, ComicForm
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
			prof=User.objects.get(username=user)
			prof1=Artist.objects.get(user=user)
			return render(request,'Skribbly/profile.html',{'profile':prof ,'profile1':prof1})
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
		print(form)
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
	print(request.method)
	if(request.method == 'POST'):
		form = ComicForm(request.POST)
		print(form.is_valid())
		if(form.is_valid()):
			form.capture_comic(request.user)
			comic_strip = ComicStrip(user=request.user, title=form.cleaned_data['title'])
			# print(comic_strip)
			comic_strip.create()
			# messages.success(request, "Successfully saved the comic strip in your profile")
			# return redirect('profile')
		else:
			print(form.errors)
			return
	form = ComicForm()
	print(form)
	return render(request = request, template_name = 'Skribbly/mywork.html', context = {"form": form})
def edit_profile(request):
	try:
		profile = request.user.artist
		user=request.user
		
	except Artist.DoesNotExist:
		profile = Artist(user=request.user)
		
	if request.method == 'POST':
		form = ArtistForm(request.POST,request.FILES, instance=profile)
		if form.is_valid():
			form.save()
			prof=Artist.objects.get(user=user)
			return render(request,'Skribbly/profile.html',{'profile':user,'profile1':prof})
		else:
			form = ArtistForm(instance=profile)
	else:
		form = ArtistForm(instance=profile)
	
	return render(request,'Skribbly/edit_profile.html',{ 'form': form})

@property
#doesn't work as it returns an object
def profile_picture_url(self):
	if self.profile_picture and hasattr(self.profile_picture,'url'):
		return self.profile_picture.url
	
	return "/images/profdem.jpg" 
