from rest_framework import serializers
from .models import Visa,Question

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'answer_text']

class VisaListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visa
        fields = ['id', 'title']
        

class VisaSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Visa
        fields = ['id', 'title', 'description', 'questions']
