from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import download_video_tiktok, MyModelViewSet
from .views import create_video,download_image

router = DefaultRouter()
router.register(r'mymodels', MyModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('a',create_video),
    path('download_image',download_image ,name='download_image'),
    path('download_video_tiktok',download_video_tiktok ,name='download_video_tiktok'),
]