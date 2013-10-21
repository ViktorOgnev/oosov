from django.core.context_processors import csrf
from django.core.mail import send_mail, EmailMessage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import  render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.utils.translation import activate

from osov.settings import EMAIL_HOST_USER, SITEMESSAGE_RECEPIENTS
from contacts.models import ContactAddress, ContactPaymentInfo, ContactRepresentatives

from .forms import ContactForm, FastContactForm
from .models import Mail

  


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
    return render_to_response(template, context,
                              context_instance=RequestContext(request))

def contacts_page(request, template_name='osov/contacts.html'):
    """
    Renders a 'Contacts' page and processes a built in contact form by sending
    an email with a form's contents to site adminstration.
    """
    activate('ru')
    context = {}
    if request.method == 'POST':
        form = FastContactForm(data=request.POST)
        if form.is_valid():
            subject = u"A message by %s ,left on OOSOV.ORG." % form.cleaned_data['name']
            message = u''.join([_(field) + ':\n\t ' + value + u'\n\n' 
                                for field, value in form.cleaned_data.iteritems()])
            
            send_mail(subject, message, EMAIL_HOST_USER, SITEMESSAGE_RECEPIENTS)
            
            return HttpResponseRedirect(reverse('contacts_send_success'))
        
    else:
        form = FastContactForm()
    
    context['form'] = form 
    try:
        context['address'] = ContactAddress.objects.values().get(pk=1)
        context['payment'] = ContactPaymentInfo.objects.values().get(pk=1)
        context['representatives'] = ContactRepresentatives.objects.values().get(pk=1)
    except:
        context['contacts_error'] = _("Cannot fetch contatc info from database.")
    context.update(csrf(request))
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
        