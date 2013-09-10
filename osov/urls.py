from django.conf.urls import patterns, include, url
from django.views.generic.detail import DetailView
from importanciator.models import ImportantContent
from django.views.generic import TemplateView
from os import path
from coltrane.views import FilteredList


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    url(r'^admin/?', include(admin.site.urls)),
    
    # Geofiltering system
    url(r'^filtered/(?P<section>\w+)/(?P<location>\w+)/?$',
        FilteredList.as_view(), name='content_filtered_by_location'),
    # Blog section
    url(r'^article', include('coltrane.urls')),
    # Photo section
    url(r'^photo', include('photogallery.urls')),
    # Video section
    url(r'^video', include('videogallery.urls')),
    # Contacts section
    url(r'^contacts/', TemplateView.as_view(template_name="osov/contacts.html"),
        name="contacts"),
    # Main page
    url(r'^/?', 'importanciator.views.render_main', name='home_page'),
    # Filtratioin by location
    url(r'^thank_you_for_application/?', 
        TemplateView.as_view(template_name="osov/thank_you.html"), name='thank_you'),
    # Django comments
    url(r'^comments/', include('django.contrib.comments.urls')),
    
    
    (r'^tinymce/', include('tinymce.urls')),
   
)
