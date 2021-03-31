from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from cart.permissions import IsCartAuthor, IsOrderAuthor
from order.models import Order
from order.serializer import OrderSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(email=request.user)
        serializer = OrderSerializer(queryset, many=True, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'retrieve']:
            permissions = [IsOrderAuthor, ]

        elif self.action in ['create']:
            permissions = [IsAdminUser, ]

        else:
            permissions = []


        return [permission() for permission in permissions]
