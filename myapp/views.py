
from rest_framework import viewsets
from .models import MyModel, Thumbail_image
from .serializers import MyModelSerializer, VideoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pytube import YouTube
from django.http import HttpResponse
from django.core.files.base import ContentFile
from rest_framework.decorators import api_view
from .serializers import VideoSerializer
from rest_framework import status
import requests
import base64
from TikTokApi import TikTokApi
import json
import asyncio


class MyModelViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MyModelSerializer

@api_view(['GET'])
def create_video(request):
    # Nhận link video từ yêu cầu gửi đến API
    video_url = request.query_params.get('youtube_link')

    # Sử dụng thư viện pytube để lấy thông tin về video từ link
    try:
        yt = YouTube(video_url)
        title = yt.title
        duration = yt.length
      
        thumbnail_urls = get_thumbnail_images(video_url)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # Tạo một đối tượng Video từ thông tin về video
    video_data = {
        'title': title,
        'duration': duration,
        'video_url': video_url,
        'thumbnail_urls':thumbnail_urls,
    }
    serializer = VideoSerializer(data=video_data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def download_image(request):
    if request.method == 'POST':
        image_url = request.data.get('img_url')  # Nhận đường dẫn từ POST request
        if image_url:
            try:
                # Tải ảnh từ URL
                response = requests.get(image_url)
                print(response)
                if response.status_code == 200:
                    # Lấy dữ liệu của ảnh
                    image_data = response.content
                    thumbnail_image = Thumbail_image.objects.create(image=image_data)
                    image = base64.b64encode(thumbnail_image.image).decode('ascii')
                    return HttpResponse(image,content_type="image/jpeg")
                else:
                    return Response("Không thể tải ảnh từ URL.", status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response("Đã xảy ra lỗi: {}".format(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response("Vui lòng cung cấp URL của ảnh.", status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response("Yêu cầu không được chấp nhận.", status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def download_video_tiktok(request):
    data = asyncio.run(get_video_example(request))
    return Response(data,status = status.HTTP_200_OK)

def get_thumbnail_images(url):
    # Thay YOUR_API_KEY bằng API key của bạn
    api_key = "AIzaSyAQ2pzFwHwnxg6ly5guvADqMoBZZOf1xWg"
    
    video_id = extract_video_id(url)
    
    # Tạo URL cho API request
    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet&id={video_id}&key={api_key}"
    
    # Gửi request GET đến API
    response = requests.get(api_url)
    
    # Xử lý kết quả
    if response.status_code == 200:
        # Parse JSON response
        data = response.json()
        print(data)
        # Lấy URL của các ảnh thu nhỏ từ kết quả
        thumbnails = data["items"][0]["snippet"]["thumbnails"]
        # Trích xuất các URL và đưa vào một list
        # thumbnail_urls = [thumbnail["url"] for thumbnail in thumbnails.values()]
        
        return thumbnails
    else:
        print("Error:", response.status_code)
        return None
    
def extract_video_id(youtube_url):
    # Tách ID từ URL
    query_string = youtube_url.split("?")[1]
    parameters = query_string.split("&")
    for parameter in parameters:
        key_value = parameter.split("=")
        if key_value[0] == "v":
            return key_value[1]
    return None

# ms_token = "xNZva2DISKvllrknq4J5Zgv7hnWkVmrOmWbp0FxGIT565m7DPtRKMkhco5kF6-D6dQPa-xiifeJ763u-CUK50UwXW94rRSnoCcsH_kkBjbU3pRVQNsxg1hpKZStWln7-MAMN5AG1a1cn_sq1wIc="

async def get_video_example(request):
    ms_token = request.GET.get('ms_token')
    async with TikTokApi() as api:
        await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)
        video = api.video(
            url="https://www.tiktok.com/@duylamvideoo/video/7355354062407208193"
        )
        video_info = await video.info()  # is HTML request, so avoid using this too much
        print(video_info)
    return json.dumps(video_info)