from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

gender_choices = [("M", "Male"), ("F", "Female"), ("O", "Others")]
class User(models.Model):
	username = models.CharField(max_length = 16, primary_key = True)
	first_name = models.CharField(max_length = 16)
	last_name = models.CharField(max_length = 16)
	gender = models.CharField(max_length = 6, choices = gender_choices)
	email = models.EmailField(max_length = 256)
	age = models.PositiveIntegerField(validators = [MinValueValidator(10), MaxValueValidator(120)])
	profile_picture = models.ImageField(upload_to = 'Skribbly/Profile Pictures/') #height_field #width_field
	date_joined = models.DateTimeField(default = timezone.now)
	favorites = models.ManyToManyField('ComicStrip', related_name = 'favorites', blank = True)

	def __str__(self):
		return self.username

class ComicStrip(models.Model):
	strip_image = models.ImageField(upload_to = 'Skribbly/Comic Strips/') #height_field #width_field
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comic_strips')
	title = models.CharField(max_length = 32)
	created_on = models.DateTimeField(default = timezone.now)
	likes = models.ManyToManyField(User, related_name = 'likes', blank = True)

	def __str__(self):
		return self.title

	def create(self):
		self.created_on = timezone.now()
		self.save()

class Comment(models.Model):
	comment = models.TextField(max_length = 512)
	edited = models.BooleanField()
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')
	comic_strip = models.ForeignKey(ComicStrip, on_delete = models.CASCADE, related_name = 'comments')
	added_on = models.DateTimeField(default = timezone.now)
	upvotes = models.ManyToManyField(User, related_name = 'upvotes', blank = True)
	downvotes = models.ManyToManyField(User, related_name = 'downvotes', blank = True)

	def add(self):
		self.added_on = timezone.now()
		self.save()
