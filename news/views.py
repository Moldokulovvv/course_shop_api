from django.shortcuts import render
from rest_framework import viewsets, generics

from news.serializers import NewsSerializer




class NewsViewSet(generics.ListCreateAPIView):

    serializer_class = NewsSerializer