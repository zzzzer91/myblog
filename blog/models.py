from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)
    img = models.ImageField(upload_to='imgs/upload', default='imgs/default/default.jpg', null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category)
    created_time = models.DateTimeField()
    modified_time = models.DateTimeField()
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """获取文章主内容url."""

        return reverse('blog:detail', kwargs={'pk': self.pk})

    def increase_views(self):
        """文章访问量加1."""

        self.views += 1
        self.save(update_fields=['views'])

    def increase_likes(self):
        """点赞数加1."""

        self.likes += 1
        self.save(update_fields=['likes'])

    class Meta:
        """根据创建文章时间逆序排序文章."""

        ordering = ['-created_time']


class About(models.Model):
    title = models.CharField(max_length=70)
    excerpt = models.CharField(max_length=200, blank=True)
    body = models.TextField()
    
    def __str__(self):
        return self.title