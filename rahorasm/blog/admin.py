from django.contrib import admin
from .models import Post, Category, Comment


# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin



admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)