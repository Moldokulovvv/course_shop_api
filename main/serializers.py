from rest_framework import serializers

from .models import Category, Course, CourseImage, Comment
from likes import services as likes_services

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CourseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseImage
        fields = '__all__'

    def _get_image_url(self, obj):
        if obj.image:
            url = obj.image.url
            request = self.context.get('request')
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''

        return url

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)

        return representation


class CourseSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)
    is_fan = serializers.SerializerMethodField()

    images = CourseImageSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ('id', 'title', 'category', 'created_at', 'text', 'is_fan', 'total_likes', 'images', 'price')

    def get_is_fan(self, obj):
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)

    def get_fields(self):
        action = self.context.get('action')
        fields = super().get_fields()


        if action == 'list':

            fields.pop('images')
        return fields

    def to_representation(self, instance):
        action = self.context.get('action')
        fields = super().get_fields()
        representation = super().to_representation(instance)
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True, context=self.context).data
        representation['author'] = instance.author.email
        representation['category'] = CategorySerializer(instance.category).data

        representation['images'] = CourseImageSerializer(instance.images.all(), many=True, context=self.context).data
        if action == 'retrieve':
            recomendation = Course.objects.filter(title__icontains=instance.title)
            recomendation_ = []
            for rec in recomendation:
                recomendation_.append(rec.title)
            representation['recomendation'] = f"{recomendation_}"
        return representation

    def create(self, validated_data):
        print(validated_data)
        request = self.context.get('request')
        user_id = request.user.id
        images_data = request.FILES


        validated_data['author_id'] = user_id
        course = Course.objects.create(**validated_data)
        for image in images_data.getlist('image'):

            CourseImage.objects.create(course=course, image=image)
        return course






class CommentSerializer(serializers.ModelSerializer):
    # created = serializers.DateTimeField(format='%d/%m/%Y %H:%M:%S', read_only=True)


    class Meta:
        model = Comment
        fields = ('body', 'course')


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = instance.author.email
        return representation

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = request.user.id
        validated_data['author_id'] = user_id
        comment = Comment.objects.create(**validated_data)
        return comment




