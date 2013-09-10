from django.shortcuts import  render_to_response
from django.core.mail import send_mail, EmailMessage
from django.core.context_processors import csrf
from django import forms
from mailit.models import Mail
from django.template import RequestContext
from osov.settings import EMAIL_HOST_USER
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse



class ContactForm(forms.Form):
    
    name = forms.CharField()
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'quote_input'})
        self.fields['email'].widget.attrs.update({'class' : 'quote_input'})
        
    


def get_list_or_post_CF(request, model, template, context={}):
    """
    Depending on request method sends an email and redirects or renders an
    object list.     
    """    
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            letter = Mail.objects.all()[0]
            to = form.cleaned_data['email']
            
            send_mail(letter.subject, letter.message, EMAIL_HOST_USER, [to,])
            return HttpResponseRedirect(reverse('thank_you'))
            
    else:
        form = ContactForm()
    context['form'] = form
    context['object_list'] = model.objects.all()
    context.update(csrf(request))
    return render_to_response(template, context, context_instance=RequestContext(request))