from django.db import models
from django.urls import reverse
from django.utils import timezone
from taggit.managers import TaggableManager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class ArchivedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.ARCHIVED)


class Post(models.Model):

    class Status(models.TextChoices):
        PUBLISHED = 'PB', 'Published'
        ARCHIVED = 'AR', 'Archive'
        DRAFT = 'DF', 'Draft'

    objects = models.Manager()
    published = PublishedManager()
    archived = ArchivedManager()

    image = models.ImageField(upload_to='blog/images/', blank=True, null=True, verbose_name='Фотография')
    title = models.CharField(max_length=127, verbose_name='Название')
    tags = TaggableManager(verbose_name='Теги', blank=True, related_name='posts')
    status = models.CharField(max_length=2, choices=Status.choices, verbose_name='Статус')
    body = models.TextField(verbose_name='Текст')
    publish = models.DateTimeField(default=timezone.now(), verbose_name='Дата публикации')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    slug = models.SlugField(max_length=255, unique_for_date='publish', verbose_name='Слаг')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year,
                                                 self.publish.month,
                                                 self.publish.day,
                                                 self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=127)
    email = models.EmailField(max_length=256)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Newsletter(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email
