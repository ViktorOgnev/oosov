from django.contrib import admin
from videogallery.models import Video

class VideoAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}
    
    
admin.site.register(Video, VideoAdmin)