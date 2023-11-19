from django.contrib import admin

from home.models import Setting, ContactFormMessage, UserProfile

# Register your models here.

admin.site.register(Setting)

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ['name','subject', 'update_at','status']
    readonly_fields =('name','subject','email','message','ip')
    list_filter = ['status']

admin.site.register(ContactFormMessage, ContactFormMessageAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_name','address', 'phone','city','country','image_tag']

admin.site.register(UserProfile, UserProfileAdmin)