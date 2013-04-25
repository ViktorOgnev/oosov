from django.conf.urls import patterns, url
from django.views.generic.list import ListView
from videogallery.models import Video
from django.views.generic.dates import DateDetailView



video_view_params = {'queryset': Video.objects.all(), 'date_field': "pub_date"}

urlpatterns = patterns('',
    

    # url(r'^/videogallery/?', ListView.as_view(model=Video),
        # name='videogallery_list'),
    url(r'^/videogallery/?', 'videogallery.views.video_list', 
        name='videogallery_list'),
   
    url(r'^/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/?$', 
            DateDetailView.as_view(**video_view_params),
            name='videogallery_video_detail'),
    
   
)