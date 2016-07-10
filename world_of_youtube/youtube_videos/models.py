from django.db import models

class Video(models.Model):
    video_title = models.CharField(max_length=250)
    video_channel = models.CharField(max_length=250)
    video_duration = models.DurationField()
    video_upload_date = models.DateField()
    video_thumbnail = models.ImageField()
    
    def __str__(self):
        return self.video_title
