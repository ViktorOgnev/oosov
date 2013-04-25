from django.contrib import admin
from mailit.models import Mail

class MailitAdmin(admin.ModelAdmin):
    
    list_display = ['subject', 'message', 'sender', 'attachement']
    ordering = ['subject', 'sender']
    
admin.site.register(Mail, MailitAdmin)