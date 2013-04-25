from django.db import models

class Mail(models.Model):
    
    subject = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    sender = models.CharField(max_length=255)
    attachement = models.FileField(upload_to="uploaded_files", blank=True, null=True)
    
    class Meta():
        verbose_name_plural = 'Letters'
    
    
    def __unicode__(self):
        return self.subject
        
    