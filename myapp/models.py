from django.db import models

class MyModel(models.Model):
    field1 = models.CharField(max_length=100)
    field2 = models.IntegerField()
    
class Thumbail_image(models.Model):
    image = models.BinaryField(blank=False,null=False)
    
    def __str__(self):
        return self.image

class Video(models.Model):
    title = models.CharField(max_length=100)
    duration = models.IntegerField()
    video_url = models.CharField(max_length=500)
    thumbnail_urls = models.JSONField()

    def __str__(self):
        return self.title