from django.db import models
from django_jalali.db import models as jmodels

class Visa(models.Model):
    title = models.CharField(max_length=200, verbose_name="نام کشور")
    description = models.TextField(verbose_name="توضیحات")
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "ویزا"
        verbose_name_plural = "ویزاها"
    
class Question(models.Model):
    visa = models.ForeignKey(Visa, related_name='questions', on_delete=models.PROTECT, verbose_name="ویزا")
    question_text = models.CharField(max_length=255, verbose_name="سوال")
    answer_text = models.TextField(verbose_name="پاسخ")
    def __str__(self):
        return self.question_text
    class Meta:
        verbose_name = "سوال و جواب ویزا"
        verbose_name_plural = "سوالات و جواب های ویزا"