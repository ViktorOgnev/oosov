from django.shortcuts import get_object_or_404, render_to_response
from importanciator.models import ImportantContent
from coltrane.models import Entry

class Content():
    def __init__(self, title, excerpt, get_a_url, url):
        self.title = title
        self.excerpt = excerpt
        self.get_absolute_url = get_a_url
        self.link = url
        


def render_main(request):
    
    object_list = []
    content_to_render = ImportantContent.objects.all()
    f_obj = None
    
    for object in content_to_render:
        if object.type == 1:
            
            f_obj_list = Entry.live.filter(title=object.title,
                                      pk=object.primary_database_identifier)
            if f_obj_list: f_obj = f_obj_list[0]
            media_url = f_obj.article_icon_thumbnail_slider
        if object.type == 2:
            pass
        if object.type == 3:
            pass
        if f_obj:
            object_to_render = Content(f_obj.title, f_obj.excerpt,
                                   f_obj.get_absolute_url(), media_url)
            object_list.append(object_to_render)
    return  render_to_response('importanciator/main_page.html',
                                     {'object_list':object_list})