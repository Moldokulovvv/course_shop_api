"""education URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

from cart.views import CartViewSet
from main.views import CategoryListView, CourseViewSet, CourseImageView, CommentViewSet

router = DefaultRouter()
router.register('courses', CourseViewSet)
router.register('comments', CommentViewSet)
router.register('cart', CartViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test descritpion",

    ),

    public=True,
)


urlpatterns = [
    path('v1/api/docs/', schema_view.with_ui()),
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework_social_oauth2.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('v1/api/categories', CategoryListView.as_view()),
    path('v1/api/add-image/', CourseImageView.as_view()),
    path('v1/api/account/', include('account.urls')),
    path('v1/api/', include(router.urls)),

] + static (settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

#https://login.vk.com/?act=openapi&oauth=1&aid=7793249%location=127.0.0.1&new=1&response_type=code