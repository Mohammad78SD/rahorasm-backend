from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django_jalali.db import models as jmodels
from django.contrib.auth import get_user_model

User = get_user_model()

class Category(models.Model):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, verbose_name="دسته بالایی")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"

class Post(models.Model):
    meta_title = models.CharField(max_length=200, verbose_name="عنوان متا")
    meta_description = models.CharField(max_length=200, verbose_name="توضیحات متا")
    title = models.CharField(max_length=200, verbose_name="عنوان")
    category = models.ManyToManyField(Category, related_name='posts', blank=True, verbose_name="دسته بندی")
    image = models.ImageField(upload_to='blog/images/', null=True, blank=True, verbose_name="تصویر")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    content = CKEditor5Field('Text', config_name='extends')
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    published = models.BooleanField(default=False, verbose_name="منتشر شده")
    
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "مطلب"
        verbose_name_plural = "مطالب"
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="مطلب")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="نویسنده")
    content = models.TextField(verbose_name="محتوا")
    created_at = jmodels.jDateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    edited_at = jmodels.jDateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    approved = models.BooleanField(default=False, verbose_name="وضعیت تایید")
    def __str__(self):
        return self.content
    class Meta:
        verbose_name = "دیدگاه"
        verbose_name_plural = "دیدگاه ها"