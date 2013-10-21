from django.contrib import admin
from .models import ContactAddress, ContactPaymentInfo, ContactRepresentatives

class ContactAdminBase(admin.ModelAdmin):
    
    class Media:
        js = ('/static/js/tiny_mce/tiny_mce.js','/static/js/tiny_mce/textareas.js')

    class Meta:
        abstract = True

class ContactAddressAdmin(ContactAdminBase):

    pass


class ContactPaymentInfoAdmin(ContactAdminBase):

    pass


class ContactRepresentativesAdmin(ContactAdminBase):

    pass

admin.site.register(ContactAddress, ContactAddressAdmin)
admin.site.register(ContactPaymentInfo, ContactPaymentInfoAdmin)
admin.site.register(ContactRepresentatives, ContactRepresentativesAdmin)
