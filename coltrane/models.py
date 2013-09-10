
import datetime
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from markdown2 import markdown
from os.path import join, splitext, split
from os import listdir
from osov.settings import SLIDER_THUMBNAIL_SIZE, STANDARD_THUMBNAIL_SIZE, IMG_UPLD_DIR, MEDIA_URL
from tagging.models import Tag
from tagging.fields import TagField
from tinymce import models as tinymce_models
from coltrane.aux_utils import transliterate, get_image_path, \
                               produce_resized_image, space_to_underscore


#---------- Comment-related imports

from akismet import Akismet
from django.conf import settings
from django.core.mail import mail_managers
from django.utils.encoding import smart_str
from django.contrib.sites.models import Site
from django.contrib.comments.models import Comment
from django.contrib.comments.signals import comment_will_be_posted
from django.contrib.comments.moderation import CommentModerator, moderator

# Fetch a Site  object so it would know where you were running the development
# server. Whenever you're  running with this database and settings file, you
# can get that Site object.

# current_site = Site.objects.get_current()
# akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                       # blog_url="http://%s/" %Site.objects.get_current().domain)



Tag.get_absolute_url = models.permalink(
              lambda self: ('coltrane_all_items_by_tag', (), {'tag': self.name.lower()}))


 
        
        
# ------------------------------------------------------------------------------
# Content, Links etc
# ------------------------------------------------------------------------------

class Location(models.Model):
    
    
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, help_text=""" Suggested value automatically 
                            generated from title. Must be unique.""")
    description = models.TextField(blank=True)
    
    
    class Meta:
        ordering = ['title']
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        
        
    def __unicode__(self):
        return self.title



class Category(models.Model):
    
    title = models.CharField(max_length=250, help_text='Maximum 250 characters.')
    slug = models.SlugField(unique=True, 
                            help_text=""" Suggested value automatically 
                            generated from title. Must be unique.""")
    description = models.TextField()
    
    
    class Meta:
        ordering = ['title']
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        
        
    def __unicode__(self):
        return self.title
    
    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_category_detail', (), {'slug': self.slug })
    
    def live_entry_set(self):
        from coltrane.models import Entry
        return self.entry_set.filter(status=Entry.LIVE_STATUS)
        

class LiveEntryManager(models.Manager):

    def get_query_set(self):
        return super(LiveEntryManager, self).get_query_set().filter(
                                                status=self.model.LIVE_STATUS)    

class Entry(models.Model):
    
    #----- Managers
    
    # custom manager enabling status based queries - becomes default, because 
    # the one daclared first will be  default
    
    live = LiveEntryManager() 
    objects = models.Manager() # standard manager(has to be reset manually)
        
    # Status constants
    
    LIVE_STATUS = 1
    DRAFT_STATUS = 2
    HIDDEN_STATUS = 3
    
    # Options for how to display a post
    
    STATUS_CHOICES = (
        (LIVE_STATUS, 'Live'),
        (DRAFT_STATUS, 'Draft'),
        (HIDDEN_STATUS, 'Hidden'),
    )
    
    # Core fields.
    article_icon = models.ImageField(upload_to=get_image_path, blank=True,  
                                     null=True)
    
    # Create a thumbnail for articles page
    article_icon_thumbnail_std = models.CharField(max_length=250,
                                                  blank=True, editable=False,
                                                  null=True)
    # Create a thumbnail for slider
    article_icon_thumbnail_slider = models.CharField(max_length=250,
                                                     blank=True, editable=False,
                                                     null=True)
    
    
    title = models.CharField(max_length=50,help_text='Maximum 50 characters.')
    excerpt = models.TextField(max_length=277,
                               blank=True, 
                               help_text= """A short summary of the entry. 
                               Maximum 277 characters. Optional.""")
    
    body = tinymce_models.HTMLField(blank=True, null=True,
                                    help_text="""You can use HTML markup - be
                                    careful!""")
    
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    
    # Date elements for easier navigation menu date archive lookup
    year = models.IntegerField(editable=False, blank=True, null=True)
    month = models.CharField(max_length=4, editable=False, blank=True, null=True)
    day = models.IntegerField(editable=False, blank=True, null=True)
    
    # Fields to store generated html.
    excerpt_html = models.TextField(editable=False, blank=True)
    body_html = models.TextField(editable=False, blank=True)
    
    # Metadata.
    author = models.ForeignKey(User)
    enable_comments = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=LIVE_STATUS)
    slug = models.SlugField(unique=True, help_text=""" Suggested value 
                        automatically generated from title. Must be unique.""")
                        
    # categorize entries
    categories = models.ManyToManyField(Category)
    tags = TagField() # tagging module http://code.google.com/p/django-tagging/
    
    # featuring location
    
    locations = models.ManyToManyField(Location)
    
    
    class Meta:
        
        verbose_name = _("Entry")
        verbose_name_plural = _("Entries")
        ordering = ['-pub_date']
    
    
    def __unicode__(self):
        return self.title
        
        
    def save(self, force_insert=False, force_update=False):
        self.body_html = markdown(self.body)
        if self.excerpt:
            if len(self.excerpt) > 277: 
                self.excerpt = (self.excerpt[0:274] + u"...")
            self.excerpt_html = markdown(self.excerpt)
            
        # It's better to save this formatting once and save RAM by using more disc
        self.year = int(self.pub_date.strftime("%Y"))
        self.month = self.pub_date.strftime("%b").lower()
        self.day =  int(self.pub_date.strftime("%d"))
        
        ai = self.article_icon
        trans_title = space_to_underscore(transliterate(self.title[0:20]))
        
        url_path, url_name = split(ai.url)
        
        # Get rid of spaces quotes etc
        url_name = space_to_underscore(url_name)
        
        url_path = join(MEDIA_URL, IMG_UPLD_DIR, trans_title)
        self.article_icon_thumbnail_slider = join(url_path, 'slider_' + url_name)
        self.article_icon_thumbnail_std = join(url_path, 'standart_' + url_name)
        
        super(Entry, self).save(force_insert, force_update)
        
        # If there's an icon provided, let's create a thumbnail for
        # a slider and for ListView
        if ai:
            # Check that we're not doing duplicate work
            # Ommitting this nested if can lead to some nasty permission issues
            # in production.
            directory, filename = split(ai.path)
            file_list = listdir(directory)
             
            if not u''.join([u'standart_', filename]) in file_list:
                
                
                # For standart representation
                produce_resized_image(  ai, STANDARD_THUMBNAIL_SIZE, trans_title,
                                        u'standart_'
                                        )
                # For Slider
                produce_resized_image(  ai, SLIDER_THUMBNAIL_SIZE, trans_title,
                                        u'slider_'
                                    )
        
        
        
        
        
        
        
    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_entry_detail', (),
               {'year': self.pub_date.strftime("%Y"),
                'month': self.pub_date.strftime("%b").lower(),
                'day' : self.pub_date.strftime("%d"),
                'slug': self.slug })
                
                
class Link(models.Model):
    
    # Metadata
    
    enable_comments = models.BooleanField(default=True)
    post_elsewhere = models.BooleanField('Post to Delicious', default=True)
    posted_by = models.ForeignKey(User)
    pub_date = models.DateTimeField(default=datetime.datetime.now)
    slug = models.SlugField(unique_for_date='pub_date',
                            help_text='Must be unique for the publication date.')
    title = models.CharField(max_length=250,
                             help_text='Maximum 250 characters')
    
    # The actual link content
    
    description = models.TextField(blank=True)
    description_html = models.TextField(editable=False, blank=True)
    url = models.URLField(unique=True)
    via_name = models.CharField('Via', max_length=250, blank=True,
                                help_text='''The name of the person whose site
                                you spotted the link on. Optional.
                                ''')
    via_url = models.URLField('Via URL', blank=True, help_text='''The URL of the
                                site where you spotted the link. Optional.''')
    
    tags = TagField()
    
    
    class Meta:
        
        ordering = ['-pub_date']
        verbose_name = _("Link")
        verbose_name_plural = _("Links")
    
    def __unicode__(self):
        return self.title
        
    def save(self, *args, **kwargs):

        if not self.id and self.post_elsewhere:
            import pydelicious
            from django.utils.encoding import smart_str
            pydelicious.add(settings.DELICIOUS_USER, settings.DELICIOUS_PASSWORD,
                            smart_str(self.url), smart_str(self.title),
                            smart_str(self.tags))
                            
        if self.description:
            self.description_html = markdown(self.description)
        
        super(Link, self).save()
        
    @models.permalink
    def get_absolute_url(self):
        return ('coltrane_link_detail', (), { 
                                'year': self.pub_date.strftime('%Y'),
                                'month': self.pub_date.strftime('%b').lower(),
                                'day': self.pub_date.strftime('%d'),
                                'slug': self.slug })
    
    

        
        
        

#---------- Comment moderation

# def moderate_comment(sender, comment, request, **kwargs):

    # """
    # comment moderation
    # """
    # # Date based.
    
    # if not comment.id:
        # entry = comment.content_object
        # delta = datetime.datetime.now() - entry.pub_date
    # if delta.days > 30:
        # comment.is_public = False
        
    # # Smart akismet moderation
    
    # if akismet_api.verify_key():
        # akismet_data = { 'comment_type': 'comment', 
                         # 'referrer': request.META['HTTP_REFERRER'],
                         # 'user_ip': comment.ip_address,
                         # 'user-agent': request.META['HTTP_USER_AGENT'],}
        # if akismet_api.comment_check(smart_str(comment.comment), akismet_data,
                                     # build_data=True):
            # comment.is_public = False
    # # Notify people via email        
    # email_body = "%s posted a new comment on the entry '%s'."
    # mail_managers("New comment posted", email_body % (comment.name,
                                                      # comment.content_object))

# # register it

# comment_will_be_posted.connect(moderate_comment, sender=Comment)


    
class EntryModerator(CommentModerator):

    auto_moderate_field = 'pub_date'
    moderate_after = 30
    email_notification = True
    
    
    def moderate(self, comment, content_object, request):
        already_moderated = super(EntryModerator, self).moderate(comment,
                                                                 content_object,
                                                                 request)
        if already_moderated:
            return True
        akismet_api = Akismet(key=settings.AKISMET_API_KEY,
                       blog_url="http:/%s/" % Site.objects.get_current().domain)
        if akismet_api.verify_key():
            akismet_data = { 'comment_type': 'comment',
                             'referrer': request.META['HTTP_REFERER'],
                             'user_ip': comment.ip_address,
                             'user-agent': request.META['HTTP_USER_AGENT'] }
            return akismet_api.comment_check(smart_str(comment.comment),
                                                       akismet_data,
                                                       build_data=True)
        return False
        
moderator.register(Entry, EntryModerator)


    
    