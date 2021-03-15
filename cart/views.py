from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from cart.models import Cart
from cart.permissions import IsCartAuthor
from cart.serializer import CartSerializer


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsCartAuthor]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(customer=request.user)
        serializer = CartSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy', 'list']:
            permissions = [IsCartAuthor, ]

        return [permission() for permission in permissions]
