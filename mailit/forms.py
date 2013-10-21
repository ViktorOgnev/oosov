from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    
    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("E-Mail"))
    
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class' : 'quote_input'})
        self.fields['email'].widget.attrs.update({'class' : 'quote_input'})
        
class FastContactForm(ContactForm):
    
    phone = forms.RegexField(label=_("Phone"),required=False, regex=r'[-+\(\)\d]+', min_length=6)
    message = forms.CharField(label=_("Message"), widget=forms.Textarea)
    
    def __init__(self, *args, **kwargs):    
        super(FastContactForm, self).__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update({'class' : 'quote_input'})
        self.fields['message'].widget.attrs.update({'class' : 'quote_input'})
        
