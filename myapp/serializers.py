from rest_framework import serializers
from .models import MyModel,Video,Thumbail_image

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = '__all__'


class YouTubeLinkSerializer(serializers.Serializer):
    youtube_link = serializers.URLField()
    
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['title', 'duration', 'video_url','thumbnail_urls'] 
        
class Thumbail_imageSerializer(serializers.Serializer):
    class Meta:
        model = Thumbail_image
        fields = '__all__'