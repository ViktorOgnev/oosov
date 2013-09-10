from django.contrib import admin
from coltrane.models import Category, Entry, Link, Location

class LocationAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}
    
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}

class EntryAdmin(admin.ModelAdmin):
   
    class Media:
        js = ('/static/js/tiny_mce/tiny_mce.js','/static/js/tiny_mce/textareas.js')
   
   
    prepopulated_fields = {'slug':['title']}
    field_options = {'classes': ['collapse', 'extrapretty'],}
    filter_horizontal = ['categories', 'locations']
    list_display = ['title','pk', 'slug', 'pub_date']
    search_fields = ['title', 'pk', 'pub_date'] 
    list_filter = ['pub_date','categories', 'locations']
    date_hierarchy = 'pub_date'
    ordering = ['-pub_date']
   
   
class LinkAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug':['title']}
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Location, LocationAdmin)
