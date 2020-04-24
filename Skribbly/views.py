from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import forms 
from .forms import CreateUserForm, ComicForm, ArtistForm, SearchForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Artist, ComicStrip, Comment
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required



# Create your views here.
def home(request):
	return render(request,'Skribbly/index.html',{'user':request.user})

def index(request):
	return redirect('home')
	
def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			# prof=User.objects.get(username=user)
			# prof1=Artist.objects.get(user=user)
			# return render(request,'Skribbly/profile.html',{'profile':prof ,'profile1':prof1})
			comics=ComicStrip.objects.filter(user=request.user)
			return render(request,'Skribbly/profile.html',{'user':user,'ComicStrips':comics[0::-1]})
		else:
			messages.info(request, 'Username OR Password is incorrect')
	return render(request,'Skribbly/login.html')
	
def logoutUser(request):
	logout(request)
	return redirect('index')

@login_required(login_url='login')
def profile(request, user):
	user = User.objects.get(username = request.user)
	comics=ComicStrip.objects.filter(user=request.user)
	return render(request,'Skribbly/profile.html',{'user':user,'ComicStrips':comics[0::-1]})

def register(request):
	form = CreateUserForm()
	if request.method =="POST":
		form = CreateUserForm(request.POST)
		#print(form)
		if form.is_valid():
			form.save()
			user = form.cleaned_data.get('username')
			messages.success(request, 'Account was created for ' + user )
			return redirect('login')
		else:
			print(form.errors)
			raise forms.ValidationError(('Invalid value-The password must be 8characters long and must not be similar to the username.Check if the passwords match'), code='invalid')

	context = {'form':form}
	return render(request,'Skribbly/register.html',context)


@login_required(login_url='login')	
def gallery(request):
	
	ComicStrips=ComicStrip.objects.all()
	cform=CommentForm()
	if(request.method=="POST"):
		form=SearchForm(request.POST)
		cform = CommentForm(request.POST)
		print(cform)
		if(form.is_valid()):
			ComicStrips=ComicStrip.objects.filter(Q(title=request.POST.get('title','')))
			#print(ComicStrips)
			return render(request,"Skribbly/gallery_search.html",{'form':form,'ComicStrips':ComicStrips})
		if(cform.is_valid()):
			return render(request,'Skribbly/gallery.htm',{'form':form,'ComicStrips':ComicStrips,'user':request.user,'cform':cform})
	else:
		form=SearchForm()
		cform=CommentForm()
		return render (request,"Skribbly/gallery.html",{'form':form,'ComicStrips':ComicStrips,'user':request.user,'cform':cform})

def tutorial(request):
	return render(request,'Skribbly/tutorial.html',{'user':request.user})
	
@login_required(login_url='login')
def canvas(request):
	user=User.objects.get(username=request.user)
	if(request.method == 'POST'):
		form = ComicForm(request.POST)
		print(form.is_valid())
		if(form.is_valid()):
			form.capture_comic(request.user)
			comic_strip = ComicStrip(user=request.user, title=form.cleaned_data['title'])
			comic_strip.create()
			# messages.success(request, "Successfully saved the comic strip in your profile")
			# return redirect('profile')
		else:
			print(form.errors)
			return
	form = ComicForm()
	print(form)
	return render(request = request, template_name = 'Skribbly/canvas.html', context = {"form": form,"user":user})

@login_required(login_url='login')
def edit_profile(request):
	user = request.user
	if request.method == 'POST':
		form = ArtistForm(request.POST,request.FILES, instance=user.artist)
		if form.is_valid():
			form.save(commit=False)
			form.save()
			comics=ComicStrip.objects.filter(user=request.user)
			return render(request,'Skribbly/profile.html',{'user':user,'ComicStrips':comics[0::-1]})
		else:
			#err=form.errors
			form = ArtistForm(instance=user.artist)
			#return render(request,'Skribbly/edit_profile.html',{ 'form': form})

	else:
		form = ArtistForm(instance=user.artist)
	
	return render(request,'Skribbly/edit_profile.html',{ 'form': form})

# @property
#doesn't work as it returns an object
# def profile_picture_url(self):
# 	if self.profile_picture and hasattr(self.profile_picture,'url'):
# 		return self.profile_picture.url
	
# 	return "/images/profdem.jpg"

def comicpage(request,pk,title):
	
	form=ComicStrip.objects.get(pk=pk)
	cform = CommentForm(request.POST)

	
	return render(request,'Skribbly/comicpage.html',{'comic':form, 'cform':cform})



	

