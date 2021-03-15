from django.db import models

from account.models import MyUser
from main.models import Course


class Cart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='cart')
    customer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='cart')


