from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

gender_choices = [("M", "Male"), ("F", "Female"), ("O", "Others")]
class Artist(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	gender = models.CharField(max_length = 6, choices = gender_choices, blank = True)
	age = models.PositiveIntegerField(null = True, validators = [MinValueValidator(10), MaxValueValidator(120)])
	profile_picture = models.ImageField(upload_to = 'Skribbly/Profile Pictures/', blank = True) #height_field #width_field
	date_joined = models.DateTimeField(default = timezone.now)
	favorites = models.ManyToManyField('ComicStrip', related_name = 'favorites')

	def __str__(self):
		return self.user.username

@receiver(post_save, sender=User)
def create_new_artist(sender, instance, created, **kwargs):
	if created:
		Artist.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_existing_artist(sender, instance, **kwargs):
    if(not instance.is_staff): instance.artist.save()

class ComicStrip(models.Model):
	strip_image = models.ImageField(upload_to = 'Skribbly/Comic Strips/') #height_field #width_field
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comic_strips')
	title = models.CharField(max_length = 64)
	created_on = models.DateTimeField(default = timezone.now)
	likes = models.ManyToManyField(User, related_name = 'likes', blank = True)

	def __str__(self):
		return self.title

	def create(self):
		# self.created_on = timezone.now()
		self.strip_image.save(f"{self.user}/{self.title}.png", open(f"media/Skribbly/Comic Strips/{self.user}/temp", 'rb'))
		os.remove(f"media/Skribbly/Comic Strips/{self.user}/temp")
		self.save()

class Comment(models.Model):
	comment = models.TextField(max_length = 512)
	edited = models.BooleanField(default = False)
	user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'comments')
	comic_strip = models.ForeignKey(ComicStrip, on_delete = models.CASCADE, related_name = 'comments')
	added_on = models.DateTimeField(default = timezone.now)
	upvotes = models.ManyToManyField(User, related_name = 'upvotes', blank = True)
	downvotes = models.ManyToManyField(User, related_name = 'downvotes', blank = True)

	def __str__(self):
		return self.comment

	def add(self):
		self.added_on = timezone.now()
		self.save()
