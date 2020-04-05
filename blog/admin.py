import markdownx.admin
from django.contrib import admin
from .models import BlogPost
from django.db import models
from django.utils import timezone

class DateCreateModMixin(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(default=timezone.now)
    mod_date = models.DateTimeField(blank=True, null=True)

class BlogPostAdmin(markdownx.admin.MarkdownxModelAdmin):
    list_display = ('title', 'created_date', 'mod_date')
    list_filter = ('created_date', 'mod_date')
    search_fields = ('title',)

admin.site.register(BlogPost, BlogPostAdmin)