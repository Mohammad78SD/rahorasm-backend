from rest_framework import generics
from .models import Post,Comment
from .serializers import PostSerializer, CommentSerializer

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostDetail(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class CommentList(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs['post_id']  # Get the post ID from the URL
        return Comment.objects.filter(post_id=post_id)  # Filter comments by post ID

    def perform_create(self, serializer):
        post_id = self.kwargs['post_id']
        post = Post.objects.get(id=post_id)  # Get the post instance
        serializer.save(author=self.request.user, post=post)  # Associate the comment with the post