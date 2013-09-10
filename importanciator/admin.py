from django.contrib import admin
from importanciator.models import ImportantContent, MainPageControl

class ImportantContentAdmin(admin.ModelAdmin):
    
    list_display = ['type', 'title', 'primary_database_identifier']
    ordering = ['type', 'primary_database_identifier']
    
class MainPageControlAdmin(admin.ModelAdmin):
    
    pass
        
admin.site.register(ImportantContent, ImportantContentAdmin)
admin.site.register(MainPageControl, MainPageControlAdmin)