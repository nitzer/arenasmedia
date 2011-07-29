# -*- coding:utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from user_profile.models import UserProfile
#from captcha.fields import CaptchaField
from django.conf import settings
from django.forms.widgets import FileInput
from django.utils.safestring import mark_safe

class ImageWidget(FileInput):
    def render(self, name, values, attrs=None):
        url = values.instance.thumb.url
        
        w = super(ImageWidget, self).render(name, values, attrs=attrs)
        return mark_safe(u"%s<img src='%s' />" % (w, url))


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=30, label=_(u"Nombre de usuario"), required=False)
    first_name = forms.CharField(max_length=30, label=_(u"Nombre(s)"), required=False)
    last_name = forms.CharField(max_length=30, label=_(u"Apellido(s)"), required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = UserProfile
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'age_range', 'date_of_birth', 'country', 'thumb', 'biography', 'web')
        widgets = {
            'biography': forms.Textarea(attrs={'cols': 45, 'rows': 10}),
            #'thumb': ImageWidget(),
        }


    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        
        if kwargs.has_key('instance'):
            instance = kwargs['instance']
            self.initial['username'] = instance.username
            self.initial['first_name'] = instance.first_name
            self.initial['last_name'] = instance.last_name
            self.initial['email'] = instance.email


    def save(self, commit=True):
        model = super(UserProfileForm, self).save(commit=False)
 
        # Save
        model.username = self.cleaned_data['username']
        model.first_name = self.cleaned_data['first_name']
        model.last_name = self.cleaned_data['last_name']
        model.email = self.cleaned_data['email']

        if commit:
            model.save()
 
        return model
