# *-* coding=utf-8 *-*

from djblog.models import Post, Category, Status, Tag
from djblog.forms import PostAdminForm
from django.contrib import admin
from django import forms
from django.db import models
from django.utils.translation import ugettext_lazy as _
from content_media.admin import MediaContentInline
from django.utils.safestring import mark_safe
from django.template.defaultfilters import timesince, timeuntil
from datetime import datetime

class BlogBaseAdmin(admin.ModelAdmin):
    save_on_top = True

    list_filter = ('pub_date', 'is_active')
    fieldsets = (
        ('Metadata config.', {
            'fields': ('meta_keywords', 'meta_description',),
            'classes': ('collapse',)
        }),
        ('Expert config.', {
            'fields': ('pub_date', 'slug', 'is_active', 'is_live', 'lang', 'site'),
            'classes': ('collapse',)
        }),
    )

    class Media:
        css = {
            'all': ('jwysiwyg/jquery.wysiwyg.css', 'jwysiwyg/jquery.wysiwyg.modal.css', 'lib/jquery.simplemodal.css')
        }
        js = ('jwysiwyg/jquery.wysiwyg.js', 'lib/jquery.simplemodal.js', 'jwysiwyg/loader.js', \
                'lib/ui/jquery.ui.core.js', 'lib/ui/jquery.ui.widget.js', 'lib/ui/jquery.ui.mouse.js', 'lib/ui/jquery.ui.resizable.js')



class PostAdmin(BlogBaseAdmin):
    list_display = ('get_category', 'title', 'status', 'author', 'pub_date', 'get_publication_date', 'get_expiration_date', 'get_is_active', 'get_is_page', 'lang')
    list_display_links = ('title',)
    list_filter = ('category', 'author', 'is_page').__add__(BlogBaseAdmin.list_filter)
    search_fields = ['title', 'copete', 'content_plain']
    form = PostAdminForm
    inlines = [MediaContentInline]
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags', 'category', 'followup_for', 'related')
    formfield_overrides = { 
        models.TextField: {'widget': forms.Textarea(attrs={'class':'wysiwyg', 'cols':'75', 'rows':'20'})}
    }

    fieldsets = (
        (None, {'fields': ('title', 'copete', 'content', 'category', 'tags', 'is_page', 'status', 'user', 'author')}),
        ('Advanced', {
            'fields': ('allow_comments', 'comments_finish_date', 'content_plain'),
            'classes': ('collapse',)
        }),
        ('Scheduling', {
            'fields': ('publication_date', 'expiration_date'),
            'classes': ('collapse',)
        }),
        ('Relationships', {
            'fields': ('followup_for', 'related'),
            'classes': ('collapse',)
        }),
    ).__add__(BlogBaseAdmin.fieldsets)

    def get_is_active(self, obj):
        if obj.is_active:
            return mark_safe('<img src="/media/img/admin/accept.png" alt="%s" />' % True)
        return mark_safe('<img src="/media/img/admin/cross.png" alt="%s" />' % False)
    get_is_active.short_description = u'activo'
    get_is_active.allow_tags = True

    def get_expiration_date(self, obj):
        if not obj.expiration_date:
            return mark_safe('<span style="color:green">nunca expira</span>')

        if obj.expiration_date and obj.expiration_date <= datetime.now():
            return mark_safe('<span style="color:orange">expiro hace %s</span>' % timesince(obj.expiration_date))
        return mark_safe('<span style="color:green">expira en %s</span>' % timeuntil(obj.expiration_date))
    get_expiration_date.allow_tags = True
    get_expiration_date.short_description = _(u"expiration_date")

    def get_publication_date(self, obj):
        if obj.publication_date and obj.publication_date <= datetime.now():
            return mark_safe('<span style="color:green">publicado hace %s</span>' % timesince(obj.publication_date))
        return mark_safe('<span style="color:blue">se publica en %s</span>' % timeuntil(obj.publication_date))
    get_publication_date.allow_tags = True
    get_publication_date.short_description = _(u"publication_date")

    def get_is_page(self, obj):
        if obj.is_page:
            return mark_safe(u'<img src="/media/img/mimes/application-xhtml+xml.png" title="Página" alt="Página" />')
        return 'Post'
    get_is_page.short_description = u'post o página'
    get_is_page.allow_tags = True

    def get_category(self, obj):
        return ', '.join([c.name for c in obj.category.all()])
    get_category.short_description = _(u'In Category')
 
    def get_tags(self, obj):
        return ', '.join([c.name for c in obj.tags.all()])
    get_tags.short_description = _(u'Tags')

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    mark_active.short_description = _(u'Mark select articles as active')

    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = _(u'Mark select articles as inactive')




class CategoryAdmin(BlogBaseAdmin):
    list_display = ('name', 'parent', 'root_level', 'get_blog_category', 'get_is_active')
    list_filter = ('root_level','blog_category',).__add__(BlogBaseAdmin.list_filter)
    prepopulated_fields = {'slug': ('name',)} 
    fieldsets = (
        (None, {'fields': ('name', 'description', 'parent')}),
        ('Advanced', {
            'fields': ('blog_category', 'root_level', 'description_plain'),
            'classes': ('collapse',)
        }),

    ).__add__(BlogBaseAdmin.fieldsets)

    def get_blog_category(self, obj):
        if obj.blog_category:
            return mark_safe('<img src="/media/img/admin/accept.png" alt="%s" />' % True)
        return mark_safe('<img src="/media/img/admin/cross.png" alt="%s" />' % False)
    get_blog_category.short_description = u'categoría de blog'
    get_blog_category.allow_tags = True


    def get_is_active(self, obj):
        if obj.is_active:
            return mark_safe('<img src="/media/img/admin/accept.png" alt="%s" />' % True)
        return mark_safe('<img src="/media/img/admin/cross.png" alt="%s" />' % False)
    get_is_active.short_description = u'activo'
    get_is_active.allow_tags = True



class StatusAdmin(BlogBaseAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name', 'description', 'is_public')}),
    ).__add__(BlogBaseAdmin.fieldsets)



class TagAdmin(BlogBaseAdmin):
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {'fields': ('name',)}),
    ).__add__(BlogBaseAdmin.fieldsets)



admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Tag, TagAdmin)
