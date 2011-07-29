# *-* coding:utf-8 *-*
"""
Una app para cargar contenidos multimedia

"""

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.contenttypes import generic
from django.utils.encoding import force_unicode
import mimetypes
import os
try:
    from PIL import Image
except ImportError:
    import Image

def_sizes = {
    'thumb': (75,75),
    'normal': (650,650)
    }

CONTENT_MEDIA_THUMBNAIL_SIZE = getattr(settings, 'CONTENT_MEDIA_THUMBNAIL_SIZE', def_sizes)
CONTENT_MEDIA_PATH = getattr(settings, 'CONTENT_MEDIA_PATH', 'mediacontent')


class MediaContentManager(models.Manager):
    def get_for_model(self, model):
        ct = ContentType.objects.get_for_model(model)
        qs = self.get_query_set().filter(content_type=ct)

        if isinstance(model, models.Model):
            qs = qs.filter(object_pk=force_unicode(model._get_pk_val()))
        return qs


class MediaContent(models.Model):
    def content_path(self, filename):
        mcls = ContentType.objects.get(pk=self.content_type.pk)
        cls = mcls.get_object_for_this_type(pk=self.object_pk)
        mimetype = mimetypes.guess_type(self.content.path)[0]
        return '%s/%s/%s/%s' % (CONTENT_MEDIA_PATH, cls._meta.module_name, mimetype, filename)
    
    def thumbpath(self, filename):
        mcls = ContentType.objects.get(pk=self.content_type.pk)
        cls = mcls.get_object_for_this_type(pk=self.object_pk)

        return '%s/%s/%s/thumb_%s' % (CONTENT_MEDIA_PATH, cls._meta.module_name, self.mimetype, filename)

    content_type = models.ForeignKey(ContentType)
    object_pk = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_pk')
    
    mimetype = models.CharField(max_length=30, editable=False)
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    
    content = models.FileField(upload_to=content_path)
    thumbnail = models.ImageField(upload_to=thumbpath, blank=True, editable=False)

    objects = MediaContentManager()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(MediaContent, self).save(args, kwargs)
        self.mimetype = mimetypes.guess_type(self.content.path)[0]
        if self.mimetype:
            content_type = self.mimetype.replace('/', '_')
        else:
            # assume everything else is text/plain
            content_type = 'text_plain'

        if not self.thumbnail and content_type.split('_')[0]=='image':
            img_path = self.content.path
            if content_type == 'image_svg+xml':
                from content_media import svg_to_png
                svg_to_png.convert(img_path, svg_to_png.new_name(img_path))
                img_path = svg_to_png.new_name(img_path)
                self.content.name = self.content.name[:-3] + self.content.name[-3:].replace('svg', 'png')

            i = self.content.name.rindex('/')
            thumb = '%sthumb_%s' % (self.content.name[:i+1], self.content.name[i+1:])
            orig = self.content.name
            self.thumbnail = thumb
            #image = Image.open(os.path.join(settings.MEDIA_ROOT, self.image.path) 

            # intenta hacer un thumb de la imagen
            image = Image.open(img_path)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
            image.thumbnail(CONTENT_MEDIA_THUMBNAIL_SIZE['thumb'], Image.ANTIALIAS)
            image.save(os.path.join(settings.MEDIA_ROOT, thumb))


            # guarda la imagen al tamaño máximo
            image = Image.open(img_path)
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
            image.thumbnail(CONTENT_MEDIA_THUMBNAIL_SIZE['normal'], Image.ANTIALIAS)
            image.save(os.path.join(settings.MEDIA_ROOT, orig))


        super(MediaContent, self).save(args, kwargs)

    def get_header(self):
        return self.mimetype.split('/')[0]
