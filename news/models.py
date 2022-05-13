from django.db import models
from djangocms_blog.models import Post


class NewsPost(Post):
    side_bar = models.BooleanField(default=None, null=True)

#
# class KoiOr(models.Model):
#     side_bar = models.BooleanField(default=None, null=True)
