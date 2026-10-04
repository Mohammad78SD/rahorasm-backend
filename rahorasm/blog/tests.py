from rest_framework.test import APITestCase
from django.urls import reverse

from test_helpers import make_user
from .models import Comment, Post


class CommentApiTests(APITestCase):
    def setUp(self):
        self.user = make_user()
        self.post = Post.objects.create(meta_title="m", meta_description="d", title="t",
                                        author=self.user, content="<p>x</p>", published=True)
        self.url = reverse("comment_list", args=[self.post.id])

    def test_anonymous_can_list(self):
        Comment.objects.create(post=self.post, author=self.user, content="hi")
        resp = self.client.get(self.url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(resp.json()), 1)

    def test_anonymous_post_is_401_not_500(self):
        """Regression: anonymous POST used to crash on request.user."""
        resp = self.client.post(self.url, {"content": "hello"})
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(Comment.objects.count(), 0)

    def test_authenticated_post_creates_comment(self):
        self.client.force_authenticate(self.user)
        resp = self.client.post(self.url, {"content": "hello"})
        self.assertEqual(resp.status_code, 201)
        c = Comment.objects.get()
        self.assertEqual((c.author, c.post, c.content), (self.user, self.post, "hello"))

    def test_post_to_missing_blog_post_is_404(self):
        self.client.force_authenticate(self.user)
        resp = self.client.post(reverse("comment_list", args=[99999]), {"content": "x"})
        self.assertEqual(resp.status_code, 404)

    def test_post_list_only_published(self):
        Post.objects.create(meta_title="m", meta_description="d", title="draft",
                            author=self.user, content="x", published=False)
        resp = self.client.get(reverse("post_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([p["title"] for p in resp.json()], ["t"])
