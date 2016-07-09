from django.shortcuts import render
from django.http import HttpResponse

from .forms import QueryForm

def index(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        
        if form.is_valid():
            country = form.cleaned_data['country']
            category = form.cleaned_data['category']
            n = form.cleaned_data['number_of_videos_to_return']
            str = "%s %s %s " % (country, category, n)
            return HttpResponse(str)
            
    else:
        form = QueryForm()
    
    return render(request, 'youtube_videos/index.html', {'form': form})
            
    