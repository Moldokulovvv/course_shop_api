from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models

from account.models import MyUser
from likes.mixins import LikedMixin
from likes.models import Like


class Category(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class Course(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = GenericRelation(Like)

    def __str__(self):
        return self.title

    @property
    def total_likes(self):
        return self.likes.count()


class CourseImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='images')


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    image = models.ImageField(upload_to='comments', blank=True)
    author = models.ForeignKey(MyUser, on_delete=models.DO_NOTHING, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.CASCADE)



    def __str__(self):
        return f'{self.course}: {self.body}'










