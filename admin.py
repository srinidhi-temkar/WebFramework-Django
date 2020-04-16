from django.contrib import admin
from .models import User, ComicStrip, Comment

admin.site.register(User)
admin.site.register(ComicStrip)
admin.site.register(Comment)