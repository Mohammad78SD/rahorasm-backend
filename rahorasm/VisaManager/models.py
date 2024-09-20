from django.db import models
from django_jalali.db import models as jmodels

class Visa(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "ویزا"
        verbose_name_plural = "ویزاها"
    
class Question(models.Model):
    visa = models.ForeignKey(Visa, related_name='questions', on_delete=models.PROTECT)
    question_text = models.CharField(max_length=255)
    answer_text = models.TextField()
    def __str__(self):
        return self.question_text
    class Meta:
        verbose_name = "سوال و جواب ویزا"
        verbose_name_plural = "سوالات و جواب های ویزا"