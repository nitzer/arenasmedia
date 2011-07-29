# *-* coding:utf-8 *-*
"""
Una app para hacer un simple blog, con posts, páginas y blocks

"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify, striptags, truncatewords, force_escape, escape, mark_safe
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datetime import datetime
from content_media.models import MediaContent
from djblog.managers import BlogManager, CategoryManager, PostManager

DJBLOG_PREVIEW_CONTENT_SIZE = getattr(settings, 'DJBLOG_PREVIEW_CONTENT_SIZE', 60) 


class BlogBase(models.Model):
    now = datetime.now()
    pub_date = models.DateTimeField(blank=True, null=True, default=now, verbose_name=_(u"Fecha de creación"))
    slug = models.SlugField(max_length=140, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_(u"Esta activo"))
    is_live = models.BooleanField(default=True, verbose_name=_(u"Esta vivo")) # no se elimina, solo de hace -invisible-
    
    lang = models.CharField(max_length=20, choices=settings.LANGUAGES, default=settings.LANGUAGE_CODE.lower(), blank=True)
    site = models.ForeignKey(Site, blank=True, null=True)

    meta_keywords = models.TextField(blank=True, help_text=_(u"opcional, para el SEO"))
    meta_description = models.TextField(blank=True, help_text=_(u"opcional, para el SEO"))

    objects = BlogManager()

    def __unicode__(self):
        if hasattr(self, 'name'):
            u = self.name
        elif hasattr(self, 'title'):
            u = self.title
        else:
            u = u"%s-%s-%s" % (self._meta.app_label, self._meta.module_name, self.pub_date)
        return u"%s" % u

    @property
    def rss_name(self):
        return u'%s/%s' % (self._meta.app_label, self.slug)

    @models.permalink
    def get_absolute_url(self):
        return (u'%s_%s' % (self._meta.app_label, self._meta.module_name), (self.slug,))
        #return u'%s_%s/%s' % (self._meta.app_label, self._meta.module_name, self.slug,)

    def save(self, *args, **kwargs):
        if not self.slug:
            if hasattr(self, 'name'):
                self.slug = slugify(self.name)
            elif hasattr(self, 'title'):
                self.slug = slugify(self.title)
            else:
                self.slug = slugify(u"%s-%s-%s" % (self._meta.app_label, self._meta.module_name, self.pub_date))

        if not self.lang:
            self.lang = settings.LANGUAGE_CODE.lower()

        if not self.site:
            self.site = Site.objects.get_current()

        return super(BlogBase, self).save(*args, **kwargs)

    class Meta:
        abstract = True
        ordering = ('-pub_date',)
        unique_together = ('slug', 'lang', 'site',)



class Tag(BlogBase):
    name = models.CharField(max_length=64, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _(u"Etiquetas")
        verbose_name = _(u"Etiqueta")



class Status(BlogBase):
    name = models.CharField(max_length=140, verbose_name=_(u"Nombre o Título"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    is_public = models.BooleanField(default=False, blank=True, help_text=_(u"Este estado determina si una publicación es visible o no"))

    class Meta:
        ordering = ('name',)
        verbose_name_plural = _(u"Estados")
        verbose_name = _(u"Estado")



class Category(BlogBase):
    name = models.CharField(max_length=40, verbose_name=_(u"Nombre o Título"))
    description = models.TextField(blank=True, verbose_name=_(u"Descripción"))
    description_plain = models.TextField(blank=True, verbose_name=_(u"Descripción en texto plano"))
    parent = models.ForeignKey('self', null=True, blank=True)
    root_level = models.PositiveIntegerField(default=0) #0 es root, 1 en adelante parent/childs
    blog_category = models.BooleanField(default=True, blank=True)

    objects = CategoryManager()

    def __unicode__(self):
        name = u"%s" % self.name
        parent = self.parent
        while parent:
            name = u"%s -> %s" % (parent.name, name)
            parent = parent.parent

        return u"%s" % name

    @models.permalink
    def get_absolute_url(self):
        slug = u"%s" % self.slug
        parent = self.parent
        while parent:
            slug = u"%s/%s" % (parent.slug, slug)
            parent = parent.parent

        slug = u"%s" % slug
        if self.blog_category:
            return (u'djblog_category', (slug,))
        else:
            return (u'djblog_noblog_category', (slug,))

    def get_category_childs(self):
        # todo las categorías childs
        cc = []
        for cat in Category.objects.filter(parent__in=[self]):
            cc.append(cat)
            cc.append(cat.get_category_childs())

        return cc

    def get_root_category(self):
        if self.parent:
            p = self.parent
            while True:
                if not p.parent: break
                p = p.parent
            return p
        else:
            return self

    def save(self, *args, **kwargs):
        """Set up root_leve and slug"""
        if self.parent:
            self.root_level = self.parent.root_level + 1
            self.blog_category = self.parent.blog_category

        self.description_plain = force_escape(striptags(force_unicode(self.description)))

        if not self.meta_description:
            self.meta_description = self.description_plain.replace('"','')

        super(Category, self).save(*args, **kwargs)
 
    class Meta:
        ordering = ('name', 'root_level', )
        verbose_name_plural = _(u"Categorías")
        verbose_name = _(u"Categoría")



class Post(BlogBase):
    title = models.CharField(max_length=140, verbose_name=_(u"Título"))
    copete = models.CharField(max_length=140, blank=True, verbose_name=_(u"Copete"))
    content = models.TextField(verbose_name=_(u"Contenido "))
    content_plain = models.TextField(blank=True, null=True, verbose_name=_(u"Contenido en texto plano"))

    is_page = models.BooleanField(default=False, blank=True, verbose_name=_(u"Mostrar como página"))

    update_date = models.DateTimeField(auto_now=True, verbose_name=_(u"Fecha de actualización"))
    publication_date = models.DateTimeField(blank=True, null=True, verbose_name=_(u"Fecha de publicación"))
    expiration_date = models.DateTimeField(blank=True, null=True, verbose_name=_(u"Fecha de vencimiento"))

    category = models.ManyToManyField(Category, blank=True, null=True)
    user = models.ForeignKey(User)
    author = models.ForeignKey(User, related_name='author')
    status = models.ForeignKey(Status, blank=True, null=True)

    tags = models.ManyToManyField(Tag, blank=True, help_text=_(u"Tags descriptívos"))
    followup_for = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='followups', verbose_name=_(u"Contenido sugerido"))
    related = models.ManyToManyField('self', blank=True, verbose_name=_(u"Contenido relacionado"))

    allow_comments = models.BooleanField(default=True, blank=True, verbose_name=_(u"Permitir comentarios"))
    comments_finish_date = models.DateTimeField(blank=True, null=True, verbose_name=_(u"Cerrar automáticamente"))

    objects = PostManager()

    class Meta:
        get_latest_by = 'publication_date'
        ordering = ('-publication_date',)
        verbose_name_plural = _(u"Posts y Páginas")
        verbose_name = _(u"Post o Página")

    def get_root_category(self):
        category = self.category.filter(root_level__gte=0)
        if category:
            return category[0].get_root_category()
        return []

    @models.permalink
    def get_absolute_url(self):
        # es una página
        if self.is_page:
            return (u'djblog_page', (self.slug,))

        # es un post noblog
        elif self.category.noblog():
            category = self.get_root_category()
            if category:
                return (u'djblog_noblog_post', (category.slug, self.slug,))

        d = self.publication_date.strftime('%Y %m %d').split()
        d.append(self.slug)
        return (u'djblog_postdate', d)
    
    def save(self, *args, **kwargs):
        
        """
        if not self.allow_comments:
            if self.is_page:
                self.allow_comments = False
            else:
                self.allow_comments = True
        """

        self.content_plain = escape(striptags(force_unicode(self.content)))

        super(Post, self).save(*args, **kwargs)

        if self.is_page or self.category.noblog():
            self.tags = ''

        if not self.meta_description:
            self.meta_description = self.content_plain.replace('"','')
        
        if not self.meta_keywords:
            self.meta_keywords = u",".join([tag.name for tag in self.tags.all()])

        if not self.publication_date:
            self.publication_date = self.pub_date

        return super(Post, self).save(*args, **kwargs)

    def get_preview_content(self):
        return mark_safe(truncatewords(self.content_plain, DJBLOG_PREVIEW_CONTENT_SIZE))
    preview_content = property(get_preview_content)

    def get_first_image(self):
        images = MediaContent.objects.get_for_model(self).filter(mimetype__startswith='image')
        if images:
            return images[0]
        return ''
    first_image = property(get_first_image)

    def get_images(self):
        images = MediaContent.objects.get_for_model(self).filter(mimetype__startswith='image')
        if images:
            return images
        return ''
    images = property(get_images)

    def get_media_content(self):
        return MediaContent.objects.get_for_model(self)
    media_content = property(get_media_content)
