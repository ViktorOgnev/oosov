from django.contrib import admin
from coltrane.models import Category, Entry, Link

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':['title']}

class EntryAdmin(admin.ModelAdmin):
   
    class Media:
        js = ('/static/js/tiny_mce/tiny_mce.js','/static/js/tiny_mce/textareas.js')
   
   
    prepopulated_fields = {'slug':['title']}
    field_options = {'classes': ['collapse', 'extrapretty'],}
    list_display = ['pk', 'title', 'slug', 'pub_date']
   
   
class LinkAdmin(admin.ModelAdmin):
   prepopulated_fields = {'slug':['title']}
    
admin.site.register(Category, CategoryAdmin)
admin.site.register(Entry, EntryAdmin)
admin.site.register(Link, LinkAdmin)
