from django.contrib import admin

from .models import *


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'publish', 'status', 'body')
    prepopulated_fields = {'slug': ('title', )}
    search_fields = ('title', 'body')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post_id', 'name', 'email', 'body', 'active', 'created')
    search_fields = ('post_id', 'name', 'email', 'body')


admin.site.register(Newsletter)

