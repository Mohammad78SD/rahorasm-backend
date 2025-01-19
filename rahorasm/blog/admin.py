from django.contrib import admin
from .models import Post, Category, Comment


# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name']
admin.site.register(Category, CategoryAdmin)

class PostAdmin(admin.ModelAdmin):
    search_fields = ['author__name']
    autocomplete_fields = ['author', 'category']
    
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)