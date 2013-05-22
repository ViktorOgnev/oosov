from django.contrib import admin
from videogallery.models import Video

class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}
    field_options = {'classes': ['collapse', 'extrapretty'],}
    list_display = ['title','pk', 'slug', 'pub_date']
    search_fields = ['pk', 'title', 'pub_date'] 
    list_filter = ['pub_date']
    date_hierarchy = 'pub_date'
    
    
    
admin.site.register(Video, VideoAdmin)