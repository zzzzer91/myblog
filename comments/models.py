from django.db import models


class Comment(models.Model):
    name = models.CharField(max_length=8)
    email = models.CharField(blank=True, max_length=40)
    url = models.CharField(blank=True, max_length=40)
    text = models.TextField(max_length=150)
    created_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post')

    def __str__(self):
        return self.text[:20]

    class Meta:
        ordering = ['-created_time']
