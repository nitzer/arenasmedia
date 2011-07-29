from django.contrib import admin
#from django.contrib.auth.admin import UserAdmin
#from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from user_profile.models import UserProfile
from user_profile.forms import UserProfileForm
from django.db import models
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

class MediaAdminImagesWidget(AdminFileWidget):
    def __init__(self, attrs={}):
        super(MediaAdminImagesWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            i = str(value.url).rindex('/')
            img_src = '%s%s' % (str(value.url)[:i+1], str(value.url)[i+1:])
            output.append('<div style="overflow:hidden; width:50px; float:right"><img src="%s" alt="" title="" width=50/></div>' % img_src)
        output.append(super(MediaAdminImagesWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))

class UserProfileAdmin(admin.ModelAdmin):
    #change_form_template = UserProfileForm
    form = UserProfileForm
    list_display = ('username', 'first_name', 'last_name', 'email', )
    #'gender', 'age_range', 'date_of_birth', 'country', 'thumb', 'biography', 'web')
    formfield_overrides = { models.ImageField: {'widget': MediaAdminImagesWidget}}

admin.site.register(UserProfile, UserProfileAdmin)
