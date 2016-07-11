from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

from .forms import QueryForm
from .models import Video

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser

from .constants import DEVELOPER_KEY, YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, COUNTRIES_DICT, CATEGORIES_DICT

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
            video_thumbnail = video_item['snippet']['thumbnails']['medium']['url'],
            video_url = "http://www.youtube.com/watch?v=" + video_item['id']
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
            request.session['country'] = country
            request.session['category'] = category
            request.session['number_of_videos'] = n
            return HttpResponseRedirect('/results.html')
        
    else:
        form = QueryForm()
    
    return render(request, 'youtube_videos/index.html', {'form': form})
    
def results(request):
    country = request.session['country']
    category = request.session['category']
    number_of_videos = request.session['number_of_videos']
    
    videos = get_popular_videos_list(country, category, number_of_videos)
    
    region = COUNTRIES_DICT[country]
    cat = CATEGORIES_DICT[int(category)]
    
    return render(request, 'youtube_videos/results.html', {'videos': videos, 'country': region, 'category': cat})
