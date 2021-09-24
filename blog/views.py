from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity

from blog.forms import EmailPostForm, CommentForm, SearchForm
from blog.models import Post, Comment


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj})


def post_detail(request, pk, slug):
    queryset = Post.published.prefetch_related('comments').filter(pk=pk, slug=slug)
    if queryset.exists():
        post = queryset.first()
    else:
        raise Http404

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            Comment.objects.create(
                name=cleaned_data['name'],
                email=cleaned_data['email'],
                body=cleaned_data['body'],
                post=post
            )
            messages.success(request, 'Comment successfully send', 'success')
        else:
            messages.error(request, 'Comment error to send', 'danger')

    return render(request, template_name='blog/post_detail.html', context={'post': post})


def reply_comment(request, post_pk, comment_pk):
    post = Post.published.get(pk=post_pk)
    comment = Comment.objects.get(pk=comment_pk, post=post)

    if request.method == 'POST':
        reply_form = CommentForm(request.POST)
        if reply_form.is_valid():
            cleaned_data = reply_form.cleaned_data
            Comment.objects.create(
                name=cleaned_data['name'],
                email=cleaned_data['email'],
                body=cleaned_data['body'],
                post=post,
                parent=comment,
                is_reply=True
            )
            messages.success(request, 'Comment successfully send', 'success')
    return redirect('blog:post-detail', post.pk, post.slug)


def post_share(request, pk):
    queryset = Post.published.filter(pk=pk)
    if queryset.exists():
        post = queryset.first()
    else:
        raise Http404

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            # Send Mail With Django
            post_url = request.build_absolute_uri(post.get_absolute_url())  # Link Domain + Link Post
            subject = f'{cleaned_data["name"]} recommends your read: {post.title}'
            message = f'Read {post.title} as {post_url}\n\n{cleaned_data["name"]}\'s comments {cleaned_data["comments"]}'

            send_mail(
                subject=subject, message=message,
                from_email=cleaned_data['from_email'],
                recipient_list=[cleaned_data['to_email']]
            )
            messages.success(request, 'Email successfully send', 'success')
            return redirect('blog:post-detail', post.pk, post.slug)
        else:
            messages.error(request, 'Email error to send', 'danger')
    else:
        form = EmailPostForm()
    return render(request, template_name='blog/post_share.html', context={'form': form, 'post': post})


def post_tag(request, pk, slug):
    tag = Tag.objects.get(pk=pk, slug=slug)
    posts = Post.published.filter(tags=tag)

    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/post_list.html', {'page_obj': page_obj, 'tag': tag})


def post_search(request):
    form = SearchForm()

    if 'query' in request.GET.keys():
        form = SearchForm(request.GET)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            query = cleaned_data['query']
            search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_query = SearchQuery(query)

            posts = Post.published.annotate(
                similarity=TrigramSimilarity(
                    'title', query
                )
            ).filter(similarity__gt=0.1).annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.3).order_by('-rank')

            return render(
                request, template_name='blog/post_search.html',
                context={'posts': posts, 'query': query, 'form': form}
            )

    return render(request, template_name='blog/post_search.html', context={'form': form})
