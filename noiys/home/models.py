from datetime import datetime
from django.contrib import *
from django.db import models
from django.contrib.auth.models import *
from django.urls.base import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch import receiver


class Task(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='task_posts')

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
     return self.title

    class Meta: 
        ordering = ['complete']

    def get_absolute_url(self):
        return reverse('post-detail', args=[self.id])        


class Comment(MPTTModel):
    task = models.ForeignKey(Task,
                             on_delete=models.CASCADE,
                             related_name='comments')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    name = models.ForeignKey(User, on_delete=models.CASCADE, max_length=50)
    content = models.TextField(max_length=1000)
    publish = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    class Meta:
        ordering = ('publish',)

    def __str__(self):
        return self.name

