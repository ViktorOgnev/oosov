from django.db import models
from markdown2 import markdown
from os.path import join, split
import datetime
from coltrane.aux_utils import get_image_path, produce_resized_image, transliterate
from osov.settings import GLRY_THUMB_SIZE, GLRY_ZOOM_IN_SIZE, MEDIA_URL, IMG_UPLD_DIR 



class Album(models.Model):

    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text=""" Suggested value automatically 
                            generated from title. Must be unique.""")
    description = models.TextField()
    
    pub_date = pub_date = models.DateTimeField(default=datetime.datetime.now, null=True, blank=True)

    
    
    class Meta:
        ordering = ['pub_date']
        verbose_name_plural = "Photo albums"
        
        
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_category_detail', (), {'slug': self.slug })
    
    def live_entry_set(self):
        from coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)
        

class Photo(models.Model):
    
    
    title = models.CharField(max_length=250,help_text='Maximum 250 characters.')
    
    # get a full description
    description = models.TextField()
    
    # cut a descripton so that it does not exceed 250 symbols
    # and fits nice in our css markup
    
    excerpt = models.TextField(blank=True, 
                            help_text='A short description. Optional.')
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    
    # make it look pretty converting it to html
    
    excerpt_html = models.TextField(editable=False, blank=True)
    description_html = models.TextField(editable=False, blank=True)
    
    slug = models.SlugField(unique=True, help_text=""" Suggested value 
                        automatically generated from title. Must be unique.""")
                        
    
    # provide an option of two mutually exclusive fields
    # accept either a link to an image or an image file itself
    
    link = models.CharField(max_length=250, blank=True, null=True, help_text='Maximum 250 characters.')
    image_file = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    
    albums = models.ManyToManyField(Album)
    
    
    # Create a thumbnail for gallery page
    url_thumbnail_std = models.CharField(max_length=250,
                                                  blank=True, editable=False,
                                                  null=True)
    url_img_zoomed_in = models.CharField(max_length=250,
                                                  blank=True, editable=False,
                                                  null=True)
    
    location = url_thumbnail_std = models.CharField(max_length=250,
                                                  blank=True, editable=False,
                                                  null=True)
    
    class Meta:
        
        verbose_name_plural = "Photos"
        ordering = ['-pub_date']
        
    def __unicode__(self):
        return self.title
        
        
    def save(self, force_insert=False, force_update=False):
        
        self.description_html = markdown(self.description)
        
        if self.excerpt:
            if len(self.excerpt) > 65: 
                self.excerpt = (self.excerpt[0:62] + u"...")
            self.excerpt_html = markdown(self.excerpt)
            

        
        f_i = self.image_file
        trans_title = transliterate(self.title[0:20])
        
        # Only if there's an image file provided
        if f_i:
            url_path, url_name = split(f_i.url)
            url_path = join(MEDIA_URL, IMG_UPLD_DIR, trans_title)
            self.url_img_zoomed_in = join(url_path, 'zoom_in_' + url_name)
            self.url_thumbnail_std = join(url_path, 'thumb_' + url_name)
        
        super(Photo, self).save(force_insert, force_update)
        
        # If there's an image file provided, let's create a thumbnail for
        # a gallery and for a zoomed view
        if f_i:
            
            # For standart representation
            produce_resized_image(  f_i, GLRY_THUMB_SIZE, trans_title,
                                    'thumb_'
                                    )
            # For Slider
            produce_resized_image(  f_i, GLRY_ZOOM_IN_SIZE, trans_title,
                                    'zoom_in_'
                                    )
    
    
    
    @models.permalink
    def get_absolute_url(self):
        return ('photogallery_photo_detail', (),
               {'year': self.pub_date.strftime("%Y"),
                'month': self.pub_date.strftime("%b").lower(),
                'day' : self.pub_date.strftime("%d"),
                'slug': self.slug })
