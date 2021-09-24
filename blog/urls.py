from django.urls import path
from blog.feeds import LatestPostsFeed

from blog.views import post_list, post_share, post_detail, reply_comment, post_tag, post_search

app_name = 'blog'

urlpatterns = [
    path('post/list/', post_list, name='post-list'),  # Posts
    path('post/detail/<int:pk>/<slug:slug>/', post_detail, name='post-detail'),  # Post
    path('post/reply/<int:post_pk>/<int:comment_pk>/', reply_comment, name='reply-comment'),  # Comment
    path('post/share/<int:pk>/', post_share, name='post-share'),  # Post-Share

    path('post/tag/<int:pk>/<slug:slug>/', post_tag, name='post-tag'),  # Post-Tags
    path('post/latest/feed/', LatestPostsFeed(), name='post-feed'),  # Feed
    path('post/search/', post_search, name='post-search'),
]
