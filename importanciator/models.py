from django.db import models

class ImportantContent(models.Model):
    
    
    # Status constants
    
    ARTICLE = 1
    VIDEO = 2
    PHOTO = 3
    
    # Options for how to display a post
    
    CONTENT_TYPE_CHOICES = (
        (ARTICLE, 'Entry'),
        (VIDEO, 'Video'),
        (PHOTO, 'Photo'),
    )
    
    
    
    primary_database_identifier = models.IntegerField()
    title = models.CharField(max_length=250,help_text='Maximum 250 characters.')
    type = models.IntegerField(choices=CONTENT_TYPE_CHOICES, default=ARTICLE)
    
    
    
    class Meta():
        verbose_name_plural = "Slider content"    