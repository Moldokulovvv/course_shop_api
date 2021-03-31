from django.db import models

from account.models import MyUser
from main.models import Course


class Favourite(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='favourites')
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='favourites')
    favourite = models.BooleanField(default=True)
