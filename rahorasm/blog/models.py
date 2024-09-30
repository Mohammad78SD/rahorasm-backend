from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

class Post(models.Model):
    meta_title = models.CharField(max_length=200)
    meta_description = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    Category = models.ManyToManyField(Category, related_name='posts', blank=True)
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = CKEditor5Field('Text', config_name='extends')
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    published = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "مطلب"
        verbose_name_plural = "مطالب"
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = jmodels.jDateTimeField(auto_now_add=True)
    edited_at = jmodels.jDateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    def __str__(self):
        return self.content
    class Meta:
        verbose_name = "دیدگاه"
        verbose_name_plural = "دیدگاه ها"