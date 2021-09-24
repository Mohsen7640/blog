from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from blog.manager import PublishedManager
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    PUBLISH = 'p'
    DRAFT = 'd'

    STATUS_CHOICES = (
        (PUBLISH, 'Published'),
        (DRAFT, 'Draft'),
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    body = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICES, default='d')

    author = models.ForeignKey(
        to=User, on_delete=models.CASCADE, related_name='posts')

    tags = TaggableManager(related_name='posts')  # taggit

    objects = models.Manager()  # Default Manager
    published = PublishedManager()  # Custom Manager

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return f'({self.author}) {self.title} -> {self.get_status_display()}'

    def get_absolute_url(self):
        return reverse(viewname='blog:post-detail', args=[self.pk, self.slug])


class Comment(models.Model):
    name = models.CharField(max_length=48)
    email = models.EmailField()
    body = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    updated_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)
    is_reply = models.BooleanField(default=False)

    post = models.ForeignKey(
        to=Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey(
        to='self', on_delete=models.CASCADE, related_name='children', null=True, blank=True)

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'

    def get_reply_comments(self):
        return self.children.filter(is_active=True).order_by('created_time')
