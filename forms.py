from django import forms
from .models import User, ComicStrip, Comment

# Register new user
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

