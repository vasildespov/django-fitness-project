from base_app.models import Article, Like, Profile
from django.contrib import admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Article)

admin.site.register(Like)