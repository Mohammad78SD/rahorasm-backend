from django.contrib import admin
from .models import Visa, Question

# You need to import this for adding jalali calendar widget
import django_jalali.admin as jadmin


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    
    
@admin.register(Visa)
class VisaAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title', 'description')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('visa', 'question_text', 'answer_text')