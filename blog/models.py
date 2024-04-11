from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.models import HitCountMixin, HitCount
from django.conf import settings
from ckeditor.fields import RichTextField

''''
This application have these models
1. Author/ user
2. Category
3. Post
4. Comment
---reply(ied) comments

'''


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    total_posts = models.IntegerField(
        editable=False, verbose_name='num of posts in this category')
    category_slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)

    @property
    def total_posts(self):
        return self.posts.filter(status='published').count()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['-created']


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=250, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='category')
    slug = models.SlugField(max_length=250)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    body = RichTextField()
    image = models.ImageField(upload_to='images/')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    hit_count_generic = GenericRelation(
        HitCount, object_id_field='object_pk', related_query_name='hit_count_generic_relation')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_app:post-detail', args=[str(self.slug)])


class BaseComment(models.Model):

    name = models.CharField(max_length=80)
    # parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        abstract = True


class Comment(BaseComment):
    comment_body = models.TextField()
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments')
    comment_slug = models.SlugField(max_length=100)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class RepliedComment(BaseComment):
    comment = models.ForeignKey(
        Comment, on_delete=models.CASCADE, related_name='reply_comments')
    reply_comment_body = models.TextField()
