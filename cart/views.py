from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from cart.models import Cart
from cart.permissions import IsCartAuthor
from cart.serializer import CartSerializer
from main.serializers import CourseSerializer
from order.models import Order


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCartAuthor]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(customer=request.user)
        print(queryset)
        serializer = CartSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

    def create(self, request, *args, **kwargs):
        a = self.get_serializer_context()
        cart = request.data
        obj = Cart.objects.filter(customer=request.user)
        courses_id = []
        for i in obj:
            courses_id.append(i.course.id)
        if int(cart['course']) in courses_id:
            return Response('Курс уже добавлен в корзину')
        else:
            serializer = CartSerializer(data=cart, context=a)
            if serializer.is_valid(raise_exception=True):
                cart_saved = serializer.save()
            return Response(serializer.data)


    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            permissions = [IsCartAuthor, ]
        else:
            permissions = []


        return [permission() for permission in permissions]






