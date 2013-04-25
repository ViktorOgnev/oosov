from django.contrib import admin
from photogallery.models import Photo, Album

class PhotoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}
    
class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}
    
    
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)