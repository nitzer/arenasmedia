from django.contrib import admin
from django.db import models
from django import forms
from django.contrib.contenttypes import generic
from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from django.conf import settings
import mimetypes
from content_media.models import MediaContent
from django.core import urlresolvers

class AdminMediaContentWidget(AdminFileWidget):
    def __init__(self, attrs={}):
        super(AdminMediaContentWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        output = []
        if value and hasattr(value, "url"):
            if mimetypes.guess_type(value.url)[0].split('/')[0] == 'image':
                i = str(value.url).rindex('/')
                img_src = '%sthumb_%s' % (str(value.url)[:i+1], str(value.url)[i+1:])
                output.append('''
                <div style="overflow:hidden; width:100px; float:right">
                <img src="%s" alt="" title="" />
                <a href="javascript:;" onclick="$('.wysiwyg').wysiwyg('insertImage', '%s');" title="agregar al contenido" class="addlink">&nbsp;</a>
                </div>''' % (img_src, value.url))
            else:
                img_src = settings.MEDIA_URL + 'img/mimes/' + mimetypes.guess_type(value.url)[0].replace('/', '-') + '.png'
                output.append('''
                <div style="overflow:hidden; width:100px; float:right">
                <img src="%s" alt="" title="" />
                </div>''' % img_src)


        output.append(super(AdminMediaContentWidget, self).render(name, value, attrs))
        return mark_safe(u''.join(output))


class MediaContentInline(generic.GenericStackedInline):
    model = MediaContent
    ct_field = 'content_type'
    ct_fk_field = 'object_pk'
    verbose_name = "Multimedia"
    verbose_name_plural = "Multimedias"
    
    extra = 1
    formfield_overrides = { 
            models.FileField: {'widget': AdminMediaContentWidget},
            models.TextField: {'widget': forms.Textarea(attrs={'cols':40, 'rows':2})}
    }
    verbose_name = u"multimedia"


class MediaContentAdmin(admin.ModelAdmin):
    list_display = ('content_type', 'get_content_object', 'title', 'get_content', 'get_mimetype')
    list_display_links = ('title',)
    exclude = ('content_type', 'object_pk')
    formfield_overrides = { 
            models.FileField: {'widget': AdminMediaContentWidget},
            models.TextField: {'widget': forms.Textarea(attrs={'cols':40, 'rows':2})}
    }
  
    fieldsets = (
        (None, {'fields': ('title', 'description', 'mimetype', 'content', 'thumbnail')}),
    )

    def get_content_object(self, obj):
        obj_url = urlresolvers.reverse('admin:%s_%s_change' % (
            obj.content_object._meta.app_label, obj.content_object._meta.module_name),
            args=(obj.content_object.id,))
        return '''<a href="%s">%s</a>''' % (obj_url, obj.content_object)
    get_content_object.short_description = 'content object'
    get_content_object.allow_tags = True

    def get_content(self, obj):
        return obj.content.name.split('/')[-1:][0]
    get_content.short_description = 'content'

    def get_mimetype(self, obj):
        img = settings.MEDIA_URL + 'img/mimes/' + obj.mimetype.replace('/', '-') + '.png'
        return '<img src="%s" align="left"/><span style="margin:5px 0 0 5px">%s</span>' % (img, obj.mimetype)
    get_mimetype.allow_tags = True
    get_mimetype.short_description = 'mimetype'



#admin.site.register(MediaContent, MediaContentAdmin)
try:
    admin.site.register(MediaContent, MediaContentAdmin)
except:
    pass
