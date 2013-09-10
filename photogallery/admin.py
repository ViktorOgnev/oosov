from django.contrib import admin
from photogallery.models import Photo, Album

class PhotoAdmin(admin.ModelAdmin):
    
    filter_horizontal = ['albums', 'locations']

    prepopulated_fields = {'slug':['title']}
    field_options = {'classes': ['collapse', 'extrapretty'],}
    list_display = ['title','pk', 'slug', 'pub_date']
    search_fields = ['pk', 'title', 'pub_date'] 
    list_filter = ['pub_date','albums']
    date_hierarchy = 'pub_date'
    ordering = ['-pub_date']
    
class AlbumAdmin(admin.ModelAdmin):
    list_filter = ['pub_date']
    prepopulated_fields = {'slug':['title']}
    date_hierarchy = 'pub_date'

    
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
