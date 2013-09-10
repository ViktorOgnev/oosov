# Create your views here.

# TODO :
# Write a view that fetches all albums and returns an objec_list
# each element of a list is a dictionary of a format 
# {album_title : [list_of_corresponding_pohtos]}
#
# There's an option of using an object instead of dict
# so that each object has a title and album(a list of photos) property
from photogallery.models import Album, Photo
from django.shortcuts import render_to_response
from coltrane.models import Location


class ObjectList():
        
        
    def __init__(self, title, list):
        self.title = title
        self.object_list = list


def render_albums(request):
    
    albums = Album.objects.all()
    result = []
    
    for album in albums:
        album_obj = ObjectList(album.title, [])
        for photo in Photo.objects.filter(albums=album.pk):
            album_obj.object_list.append(photo)
            
        result.append(album_obj)
            
    return render_to_response('photogallery/photo_list.html', 
                              {'object_list': result,
                               'locations' : Location.objects.all(),
                               'section': 'photo'}) 