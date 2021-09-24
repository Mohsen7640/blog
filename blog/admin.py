from django.contrib import admin
from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'publish', 'status')
    list_filter = ('status', 'author__username')
    search_fields = ('title', 'body')
    list_editable = ('status',)
    ordering = ('-publish',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'post', 'is_reply', 'is_active')
    list_filter = ('is_active',)
    list_editable = ('is_reply', 'is_active',)
    ordering = ('-created_time',)
