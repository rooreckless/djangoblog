# モデル
from django.db import models
# created_a
from .generic.timestamp import TimeStampedModel


class Blog(TimeStampedModel):
    title = models.CharField(verbose_name='title', blank=False, null=False, max_length=255)
    contents_text = models.TextField(
        verbose_name='contents_text',
        blank=True,
        null=True,
        max_length=1000,
    )
    def __str__(self):
        return self.title