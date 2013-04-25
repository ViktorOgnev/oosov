from django.conf.urls import patterns, include, url
from django.views.generic.detail import DetailView
from importanciator.models import ImportantContent
from django.views.generic import TemplateView
from os import path


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'osov.views.home', name='home'),
    # url(r'^osov/', include('osov.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/?', include(admin.site.urls)),
    url(r'^article', include('coltrane.urls')),
    url(r'^photo', include('photogallery.urls')),
    url(r'^video', include('videogallery.urls')),
    url(r'^contacts/', TemplateView.as_view(template_name="osov/contacts.html"),
        name="contacts"),
    
    url(r'^/?', 'importanciator.views.render_main', name='home_page'),
    url(r'^thank_you_for_application/?', 
        TemplateView.as_view(template_name="osov/thank_you.html")),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^tinymce/', include('tinymce.urls')),
   
)
