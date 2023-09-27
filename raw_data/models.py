from django.db import models


class NewsData(models.Model):
  title = models.CharField(max_length=1000)
  content = models.TextField()

  def __str__(self):
      return self.title
  