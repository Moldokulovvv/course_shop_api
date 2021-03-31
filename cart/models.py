from django.db import models

from account.models import MyUser
from main.models import Course
from order.models import Order


class Cart(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='carts')
    customer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='cart')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='cartss')



    def __str__(self):
        return f"{self.course}"


