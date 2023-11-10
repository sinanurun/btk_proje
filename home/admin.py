from django.contrib import admin

from home.models import Setting, ContactFormMessage

# Register your models here.

admin.site.register(Setting)

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

admin.site.register(ContactFormMessage, ContactFormMessageAdmin)