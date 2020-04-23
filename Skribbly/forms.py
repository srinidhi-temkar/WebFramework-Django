from django import forms
from django.forms import ModelForm
from .models import Artist, ComicStrip, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
import base64
import os

# # Register new user
# class RegisterForm(forms.ModelForm):
# 	class Meta:
# 		model = User

# # Login existing user
# class LoginForm(forms.ModelForm):
# 	class Meta:
# 		model = User

# Create/Upload new comic strip
class ComicForm(forms.Form):
	title = forms.CharField(label = "Title of the Comic Strip", max_length = 64)
	image_data = forms.CharField(widget=forms.HiddenInput(), required = False)

	def capture_comic(self, user):
		dataUrlPattern = re.compile('data:image/(png);base64,(.*)$')
		image_data = self.cleaned_data['image_data']
		image_data = dataUrlPattern.match(image_data).group(2)
		image_data = image_data.encode()
		image_data = base64.b64decode(image_data)
		try:
			os.makedirs(f"media/Skribbly/Comic Strips/{user}")
		except FileExistsError:
			pass
		with open(f'media/Skribbly/Comic Strips/{user}/temp', 'wb') as f:
		    f.write(image_data)

# Add new comment or edit existing comment
class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['comment', 'user', 'edited', 'comic_strip', 'upvotes', 'downvotes']

# Search existing comic strips
class SearchForm(forms.ModelForm):
	class Meta:
		model = ComicStrip
		fields = ['title']

class ArtistForm(forms.ModelForm):
	class Meta:
		model = Artist
		fields = ['gender','age','profile_picture']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username','email','password1','password2']
