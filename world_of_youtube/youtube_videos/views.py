from django.shortcuts import render, render_to_response
from django.http import HttpResponse

from .forms import QueryForm
from .models import Video

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from .constants import DEVELOPER_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION

# from iso8601 import parse_date
from isodate import parse_date, parse_duration

def parse_upload_date(upload_date):
    """ Returns a datetime object for an upload date in ISO8601 format
   
        upload_date: upload_date of a youtube video
    """
    return parse_date(upload_date)
    
def parse_video_duration(duration):
    """ Returns a datetime object for a video duration in ISO8601 format
    
        duration: the length of the video
    """
    return parse_duration(duration)

def get_popular_videos_list(region_code, video_category, number_of_videos_wanted):
    """
    Retrieves a list of popular videos given a region, category
    and the number of videos to return.
    
    region_code: The region from which to retrieve the most popular videos
    video_category: The category from which to select the most popular videos
    number_of_videos_wanted: The number of videos to return
    """
    
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)
    
    results = youtube.videos().list(
        part="snippet,contentDetails",
        regionCode=region_code,
        maxResults=number_of_videos_wanted,
        chart="mostPopular",
        videoCategoryId=video_category
    ).execute()
    
    list_of_videos = []
    for video_item in results.get('items', []):
        video = Video(
            video_title = video_item['snippet']['title'],
            video_channel = video_item['snippet']['channelTitle'],
            video_duration = parse_video_duration(video_item['contentDetails']['duration']),
            video_upload_date = parse_upload_date(video_item['snippet']['publishedAt']),
            video_thumbnail = video_item['snippet']['thumbnails']['default']['url']
        )
        list_of_videos.append(video)
    return list_of_videos

def index(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        
        if form.is_valid():
            country = form.cleaned_data['country']
            category = form.cleaned_data['category']
            n = int(form.cleaned_data['number_of_videos_to_return'])
            videos = get_popular_videos_list(country, category, n)
            return render_to_response('youtube_videos/index.html', {'videos': videos})
            
    else:
        form = QueryForm()
    
    return render(request, 'youtube_videos/index.html', {'form': form})
    
            
    