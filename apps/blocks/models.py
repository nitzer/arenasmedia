# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.sites.models import Site
from django.conf import settings
from django.template.defaultfilters import slugify, striptags
from django.utils.translation import ugettext as _

DEFAULT_LANGUAGE = getattr(settings, 'LANGUAGE_CODE', 'en')

if DEFAULT_LANGUAGE not in settings.LANGUAGES:
    DEFAULT_LANGUAGE = DEFAULT_LANGUAGE.split('-')[0]

class BlockManager(models.Manager):
    # por defecto filtro los blockes activos
    def filter(self, *args, **kwargs):
        if not kwargs.has_key('status') or kwargs['status']=='':
            kwargs['status'] = True
        return self.get_query_set().filter(*args, **kwargs)

    def filter_or_default(self, *args, **kwargs):
        if not kwargs.has_key('lang') or not kwargs['lang']:
            kwargs['lang'] = DEFAULT_LANGUAGE
        qs = self.get_query_set().filter(*args, **kwargs)
        return qs


class Block(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('Block Name'))
    block_key = models.SlugField(help_text=_('Block Key Identifier, together with lang must be unique. Use this key to call from template'))
    lang = models.CharField(max_length=20, default=DEFAULT_LANGUAGE, choices=settings.LANGUAGES)
    status = models.BooleanField(default=True, blank=True, verbose_name=_('Is Active'))
    content = models.TextField()

    objects = BlockManager()

    def __unicode__(self):
        return self.name

    class Meta:
        unique_together = ('block_key', 'lang')
