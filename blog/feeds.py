from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.template.defaultfilters import truncatewords
from blog.models import Post


class LatestPostsFeed(Feed):
    title = 'XBlog'
    link = reverse_lazy('blog:post-list')
    description = 'New Posts on XBlog'

    def items(self):
        return Post.published.order_by('-publish')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.body, 30)
