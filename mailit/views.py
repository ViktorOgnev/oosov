from django.shortcuts import  render_to_response
from django.core.mail import send_mail
from django.core.context_processors import csrf
from django import forms
from mailit.models import Mail
from django.template import RequestContext

class ContactForm(forms.Form):
    
    name = forms.CharField()
    email = forms.EmailField()
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'quote_input'})
        self.fields['email'].widget.attrs.update({'class' : 'quote_input'})
        



def get_list_or_post_CF(request, model, template):
    if request.method == 'POST':
        form = ContactForm(data=request.POST)
        if form.is_valid():
            letter = Mail.objects.all()[0]
            to = (form.cleaned_data['email'],)
            send_mail(letter.subject, letter.message, letter.sender,
                       to)
            return HttpResponseRedirect(reverse('osov_thank_you'))
    else:
        form = ContactForm()
    c =  {'form': form, 'object_list' : model.objects.all()} 
    c.update(csrf(request))
    return render_to_response(template, c, context_instance=RequestContext(request))