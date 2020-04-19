from django import forms
from django.forms import ModelForm
from .models import Artist, ComicStrip, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Register new user
"""
class RegisterForm(forms.ModelForm):
	class Meta:
		model = User

# Login existing user
class LoginForm(forms.ModelForm):
	class Meta:
		model = User

# Create/Upload new comic strip
class ComicForm(forms.ModelForm):
	class Meta:
		model = ComicStrip	

# Add new comment or edit existing comment
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment

# Search existing comic strips
class SearchForm(forms.ModelForm):
	class Meta:
		model = ComicStrip
"""

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']
