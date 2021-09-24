from django import template
from django.db.models import Count, Q
from markdown import markdown
from django.utils.safestring import mark_safe

from blog.forms import CommentForm
from blog.models import Post

register = template.Library()


# Custom Template
@register.simple_tag
def get_count_post_published():
    return Post.published.count()  # Str


@register.inclusion_tag('blog/partial/latest_posts.html')
def get_latest_post_published(limit=4):
    latest_posts = Post.published.order_by('-publish')[:limit]
    return {'latest_posts': latest_posts}


@register.inclusion_tag('blog/partial/similar_posts.html')
def get_similar_post_published(pk):
    post = Post.published.filter(pk=pk).first()
    tags_ids = post.tags.values_list('id', flat=True)  # <QuerySet [1, 2, 3]>
    similar_posts = Post.published.filter(tags__id__in=tags_ids).exclude(pk=pk).distinct().annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', '-publish')[:4]

    return {'similar_posts': similar_posts}


@register.inclusion_tag('blog/partial/taggit.html')
def get_post_published(pk):
    post = Post.published.filter(pk=pk).first()
    return {'post': post}


@register.inclusion_tag('blog/partial/comments.html')
def get_comments_is_active(pk):
    post = Post.published.filter(pk=pk).first()
    comments = post.comments.filter(is_active=True, is_reply=False)

    return {'post': post, 'comments': comments, 'form': CommentForm, 'reply_form': CommentForm}


@register.simple_tag
def get_most_commented_posts(limit=4):
    original_comments = Count(
        'comments',
        filter=Q(comments__is_reply=False, comments__is_active=True)
    )
    reply_comments = Count(
        'comments',
        filter=Q(comments__is_reply=True, comments__is_active=True)
    )
    return Post.published.annotate(
        total_comments=original_comments + reply_comments
    ).order_by('-total_comments')[:limit]  # QuerySet


# Custom Filter
@register.filter(name='markdown')
def markdown_formatter(text):
    return mark_safe(markdown(text))
