from django.contrib import admin
from .models import Artist, ComicStrip, Comment

admin.site.register(Artist)
admin.site.register(ComicStrip)
admin.site.register(Comment)