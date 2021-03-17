from datetime import timedelta

from django.utils import timezone
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated, IsAdminUser
from likes.mixins import LikedMixin
from .permissions import IsCourseAuthor
from django.db.models import Q
from django.shortcuts import render
from rest_framework.decorators import api_view, action

from main.models import Category, Course, CourseImage, Comment
from main.serializers import CategorySerializer, CourseSerializer, CourseImageSerializer, CommentSerializer


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny, ]



class CourseViewSet(LikedMixin,viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = (IsAdminUser, )

    def get_serializer_context(self):
        return {'request': self.request, 'action':self.action}

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'search']:
            permissions = [AllowAny, ]

        elif self.action in ['like', 'unlike', 'fans']:
            permissions = [IsAuthenticated, ]
        else:
            permissions = [IsAdminUser, ]
        return [permission() for permission in permissions]

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update', 'destroy']:
    #         permissions = [IsCourseAuthor, ]
    #     else:
    #         permissions = []
    #     return [permission() for permission in permissions]

    @action(detail=False, methods=['get'])
    def my_courses(self, request):
        queryset = self.get_queryset()
        queryset = queryset.filter(author=request.user)
        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        weeks_count = int(self.request.query_params.get('day', 0))
        if weeks_count > 0:
            start_date = timezone.now() - timedelta(days=weeks_count)
            queryset = queryset.filter(created_at__gte=start_date)
        return queryset


    @action(detail=False, methods=['get'])    #router builds path posts/search/?q=paris
    def search(self, request, pk=None):

        q = request.query_params.get('q')        #request.query_params = request.GET
        queryset = self.get_queryset() #->Post.objects.all()
        queryset = queryset.filter(Q(title__icontains=q) |
                                   Q(text__icontains=q))
        serializer = CourseSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)









class CourseImageView(generics.ListCreateAPIView):
    queryset = CourseImage.objects.all()
    serializer_class = CourseImageSerializer

    def get_serializer_context(self):
        return {'request': self.request}

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_serializer_context(self):
        return {'request': self.request}