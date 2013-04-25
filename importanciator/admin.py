from django.contrib import admin
from importanciator.models import ImportantContent

class ImportantContentAdmin(admin.ModelAdmin):
    
    list_display = ['type', 'title', 'primary_database_identifier']
    ordering = ['type', 'primary_database_identifier']
    
admin.site.register(ImportantContent, ImportantContentAdmin)