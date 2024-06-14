from django.db import models

from app_author.models import Author


class Quote(models.Model):
    quote = models.TextField()
    tags = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="quotes", on_delete=models.CASCADE)

