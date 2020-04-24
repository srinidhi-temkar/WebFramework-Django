from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
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
			comic_strips = ComicStrip.objects.filter(user=request.user)
			return render(request,'Skribbly/profile.html',{'user':user,'comics':comic_strips[0::-1]})
		else:
			messages.info(request, 'Username OR Password is incorrect')
	return render(request,'Skribbly/login.html')
	
def logoutUser(request):
	logout(request)
	return redirect('index')

@login_required(login_url='login')
def profile(request, username):
	user = User.objects.get(username = username)
	comic_strips = ComicStrip.objects.filter(user=user)
	return render(request,'Skribbly/profile.html',{'user':user,'comics':comic_strips[0::-1]})

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

@login_required(login_url = 'login')
def like(request):
	user = request.user
	pk = request.POST.get('comic_strip_pk')
	comic_strip = ComicStrip.objects.get(pk=pk)
	_liked = user in comic_strip.likes.all()
	if _liked:
		comic_strip.likes.remove(user)
	else:
		comic_strip.likes.add(user)
	return JsonResponse({'liked':_liked, 'comic_strip_pk':pk})

@login_required(login_url = 'login')
def favorite(request):
	user = request.user
	pk = request.POST.get('comic_strip_pk')
	comic_strip = ComicStrip.objects.get(pk=pk)
	_favorited = comic_strip in user.artist.favorites.all()
	if _favorited:
		user.artist.favorites.remove(comic_strip)
	else:
		user.artist.favorites.add(comic_strip)
	return JsonResponse({'favorited':_favorited, 'comic_strip_pk':pk})

def gallery(request):
	user = request.user
	if(request.method == "POST"):
		print(request.POST)
		if('title' in request.POST):
			search_form = SearchForm(request.POST)
			comment_form = CommentForm()
			if(search_form.is_valid()):
				comic_strips = ComicStrip.objects.filter(Q(title=request.POST.get('title','')))
				return render(request,'Skribbly/gallery.html',{'search_form':search_form,'comic_strips':comic_strips,'user':user,'comment_form':comment_form})
			else:
				return render(request,'Skribbly/gallery.html',{'search_form':search_form,'comic_strips':comic_strips,'user':user,'comment_form':comment_form})
		elif('comment' in request.POST):
			if(user.is_authenticated):
				comment_form = CommentForm(request.POST)
				search_form = SearchForm()
				comic_strips = ComicStrip.objects.all()
				if(comment_form.is_valid()):
					comment = comment_form.save(commit = False)
					comment.user = user
					comment.comic_strip = ComicStrip.objects.get(pk = request.POST['comic_strip'])
					comment.save()
					comment_form = CommentForm()
					# change to profile
					return render (request,"Skribbly/gallery.html",{'search_form':search_form,'comic_strips':comic_strips,'user':user,'comment_form':comment_form})
				else:
					print(comment_form.errors)
					return render (request,"Skribbly/gallery.html",{'search_form':search_form,'comic_strips':comic_strips,'user':user,'comment_form':comment_form})
			else:
				return redirect('login')
	else:
		search_form = SearchForm()
		comment_form = CommentForm()
		comic_strips = ComicStrip.objects.all()
		return render (request,"Skribbly/gallery.html",{'search_form':search_form,'comic_strips':comic_strips,'user':user,'comment_form':comment_form})

def tutorial(request):
	return render(request,'Skribbly/tutorial.html',{'user':request.user})
	
@login_required(login_url='login')
def canvas(request):
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
	return render(request = request, template_name = 'Skribbly/canvas.html', context = {"form": form,"user":request.user})

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

def comicpage(request,pk,title):
	
	form=ComicStrip.objects.get(pk=pk)
	cform = CommentForm(request.POST)

	
	return render(request,'Skribbly/comicpage.html',{'comic':form, 'cform':cform})



	

