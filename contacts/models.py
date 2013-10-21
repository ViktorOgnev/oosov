import datetime

from django.db import models
from django.utils.translation import ugettext as _


from tinymce import models as tinymce_models


class ContactBase(models.Model):

    body = tinymce_models.HTMLField(blank=True, null=True,
                                    help_text=_("""You can use HTML markup - be
                                    careful!"""),
                                    verbose_name=_("Contact information"))
    date_updated = models.DateTimeField(default=datetime.datetime.now,
                                        verbose_name=_("Date of update"))

    class Meta:
        abstract = True
        
    def save(self, force_insert=False, force_update=False):
        try:
            if len(list(self.objects.all())) > 1:
                raise ValidationError(_("Cannot have more than one instance of %"%self.unicode()))
        except:
            pass
        super(ContactBase, self).save(force_insert, force_update)

    
class ContactAddress(ContactBase):

    def __unicode__(self):
        return _("Address")
    
    class Meta:
        verbose_name = _("Adress")
        verbose_name_plural = _("Adress")

class ContactPaymentInfo(ContactBase):

    def __unicode__(self):
        return _("Payment Options")
    
    
    class Meta:
        verbose_name = _("Payment Options")
        verbose_name_plural = _("Payment Options")

class ContactRepresentatives(ContactBase):

    def __unicode__(self):
        return _("Representatives")
        
    class Meta:
        verbose_name = _("Representatives")
        verbose_name_plural = _("Representatives")
