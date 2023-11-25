from django.contrib.auth.models import User
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import ModelForm, TextInput, Textarea
from django.http import request
from django.utils.safestring import mark_safe

# Create your models here.
class Setting(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    company = models.CharField(max_length=50)
    address = models.CharField(blank=True, max_length=100)
    phone = models.CharField(blank=True, max_length=15)
    fax = models.CharField(blank=True, max_length=15)
    email = models.CharField(blank=True, max_length=50)
    smtpserver = models.CharField(blank=True, max_length=50)
    smtpemail = models.CharField(blank=True, max_length=50)
    smtppassword = models.CharField(blank=True, max_length=10)
    smtpport = models.CharField(blank=True, max_length=5)
    icon = models.ImageField(blank=True, upload_to='images/')
    facebook = models.CharField(blank=True, max_length=50)
    instagram = models.CharField(blank=True, max_length=50)
    twitter = models.CharField(blank=True, max_length=50)
    youtube = models.CharField(blank=True, max_length=50)
    aboutus = RichTextUploadingField()  # models.TextField()
    contact = RichTextUploadingField()
    references = RichTextUploadingField()
    status = models.CharField(max_length=10, choices=STATUS)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# iletisim mesajları için model

class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank=True, max_length=20)
    email = models.CharField(blank=True, max_length=50)
    subject = models.CharField(blank=True, max_length=50)
    message = models.TextField(blank=True, max_length=255)
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# class ContactForm(ModelForm):
#     class Meta:
#         model = ContactFormMessage
#         fields = ['name', 'email', 'subject','message']
#         widgets = {
#             'name'   : TextInput(attrs={'class': 'input','placeholder':'Name & Surname'}),
#             'subject' : TextInput(attrs={'class': 'input','placeholder':'Subject'}),
#             'email'   : TextInput(attrs={'class': 'input','placeholder':'Email Address'}),
#             'message' : Textarea(attrs={'class': 'input','placeholder':'Your Message','rows':'5'}),
#         }

class ContactForm(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(
                attrs={'type': "text",'class': "form-control", 'id': "name", 'placeholder': "Your Name", 'required': "required",
                       'data-validation-required-message ': "Please enter your name"}),
            'email': TextInput(
                attrs={'type': 'email', 'class': "form-control", 'id': "email", 'placeholder': "Your Email",
                       'required': "required", 'data-validation-required-message': "Please enter your email"}),
            'subject': TextInput(
                attrs={'type': "text", 'class': "form-control", 'id': "subject", 'placeholder': "Subject",
                       'required': "required", 'data-validation-required-message': "Please enter a subject"}),
            'message': Textarea(attrs={'class': "form-control", 'rows': "6", 'id': "message", 'placeholder': "Message",
                                       'required': "required",
                                       'data-validation-required-message': "Please enter your message"}),
        }

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=50)
    image = models.ImageField(blank=True, upload_to='images/users/')
    def __str__(self):
        return self.user.username
    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

@receiver(post_save, sender=User)
def create_user_profile(sender,instance,created,**kargs):
    if created:
        UserProfile.objects.create(user=instance)


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']