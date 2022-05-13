from django.contrib import admin

from djangocms_blog.admin import PostAdmin
from djangocms_blog.models import Post
from news.models import NewsPost


class CustomPostAdmin(PostAdmin):
    list_display = ['id']


admin.site.register(NewsPost)
# admin.site.unregister(Post)
# admin.site.register(Post, CustomPostAdmin)
