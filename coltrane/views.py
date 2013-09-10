from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic.list import ListView
from django.views.generic.dates import ArchiveIndexView
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse
from django.core.mail import send_mail

from coltrane.models import Entry, Category, Link, Location
from photogallery.models import Photo, Album
from videogallery.models import Video
from importanciator.models import ImportantContent
from photogallery.views import ObjectList
from mailit.views import ContactForm 
from mailit.models import Mail
from osov.settings import EMAIL_HOST_USER



class EntryList(ArchiveIndexView, FormView):
    
    form_class = ContactForm
    success_url = r'thank_you_for_application/'
    
    def form_valid(self, form):
        if form.is_valid():
            letter = Mail.objects.all()[0]
            to = form.cleaned_data['email']
            
            send_mail(letter.subject, letter.message, EMAIL_HOST_USER, [to,])
        return super(EntryList, self).form_valid(form)
        
        
    def get_context_data(self, **kwargs):
        context = super(EntryList, self).get_context_data(**kwargs)
        
        context['section'] = 'entry'
        context['locations'] = Location.objects.all()
        context['object_list'] = context['latest']
        return context
        
    
        
class FilteredList(ListView):
    
    def get_filter_attr(self):
    
        section = self.kwargs['section']
        location = self.kwargs['location']
        
        # The complexity is with photos because of nesting in Albums
        location_title = Location.objects.filter(slug=location) 
        if section == 'photo':
        
            templt_name = 'photogallery/photo_list.html'
            albums = Album.objects.filter(locations=location_title)
            queryset = []
            
            for album in albums:
                album_obj = ObjectList(album.title, [])
                for photo in Photo.objects.filter(albums=album.pk, locations=location_title):
                    album_obj.object_list.append(photo)
                queryset.append(album_obj)
        else:
            if section == 'importantcontent':
                qmodel = ImportantContent
                templt_name = 'coltrane/entry_archive.html'
            elif section == 'entry': 
                qmodel = Entry
                templt_name = 'coltrane/entry_archive.html'
            elif section == 'video':
                qmodel = Video
                templt_name = 'videogallery/video_list.html'
            
               
            queryset = qmodel.objects.filter(locations=location_title)
                
        
        return queryset, templt_name
        
        
    def get_queryset(self):
        queryset, _ = self.get_filter_attr()
        return queryset
    
    def get_template_names(self):
        _, name = self.get_filter_attr()
        return [name]
    
    def get_context_data(self, **kwargs):
        
        context = super(FilteredList, self).get_context_data(**kwargs)
        
        context['object_list'] = self.get_queryset()
        context['section'] = self.kwargs['section']
        context['locations'] = Location.objects.all()
        return context
    
    
        

def entry_index(request): 
    return render_to_response('coltrane/entry_archive.html', 
                              {'latest': Entry.live.all()})
                                
def entry_detail(request, year, month, day, slug):
    import datetime, time
    date_stamp = time.strptime(year+month+day, "%Y%b%d")
    pub_date = datetime.date(*date_stamp[:3])
    entry = get_object_or_404(Entry, pub_date__year=pub_date.year,
                              pub_date__month=pub_date.month,
                              pub_date__day=pub_date.day,
                              slug=slug)
    
    return render_to_response('coltrane/entry_detail.html',
    { 'entry': entry })
        
                                          
                                                
def category_list(request):
    return render_to_reponse('coltrane/category_list.html', 
                             {'object_list' : Category.objects.all()})
                              
def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    object_list = category.live_entry_set()
    return render_to_response('coltrane/category_detail.html',
                              { 'category': category,
                                'object_list':object_list})
                                
def all_items_by_tag(request, tag):
    tagged_entries = [e for e in Entry.live.all() if tag in e.tags]
    tagged_links = [l for l in Link.objects.all() if tag in l.tags]
    return render_to_response('coltrane/tagging/items_by_tag.html',
                                {'tagged_entries': tagged_entries,
                                  'tagged_links': tagged_links,
                                  'tagname': tag})
                                  

                                  

