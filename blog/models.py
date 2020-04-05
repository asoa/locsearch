import markdownx.utils
from django.db import models
from markdownx.models import MarkdownxField
from datetime import datetime
from django.utils import timezone


class DateCreateModMixin(models.Model):
    class Meta:
        abstract = True

    created_date = models.DateTimeField(default=timezone.now)
    mod_date = models.DateTimeField(blank=True, null=True)

# class BlogPost(DateCreateModMixin):
#     title = models.CharField(max_length=50)
#     body = MarkdownxField()
#     background_image = models.ImageField(default='img/header.jpg', upload_to=datetime.now().strftime('backgrounds/%Y/%m/%d'))


class BlogPost(DateCreateModMixin):
    title = models.CharField(max_length=50)
    body = MarkdownxField()
    background_image = models.ImageField(default='img/header.jpg', upload_to=datetime.now().strftime('backgrounds/%Y/%m/%d'))

    def formatted_markdown(self):
        return markdownx.utils.markdownify(self.body)

    def body_summary(self):
        return markdownx.utils.markdownify(self.body[:300] + "...")

