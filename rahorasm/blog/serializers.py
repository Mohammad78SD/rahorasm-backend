from rest_framework import serializers
from .models import Post, Category, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name']
        
class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.name')
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = Comment
        fields = '__all__'
        
class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.SerializerMethodField()
    category = CategorySerializer(many=True)
    author = UserSerializer()
    def get_created_at(self, obj):
        jdate = obj.created_at
        return jdate.togregorian()
    class Meta:
        model = Post
        fields = '__all__'