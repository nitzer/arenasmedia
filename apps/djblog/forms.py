# *-* coding=utf-8 *-*

from django import forms
from django.utils.translation import ugettext_lazy as _
from djblog.models import Post, Tag
from django.template.defaultfilters import slugify

class PostAdminForm(forms.ModelForm):

    content = forms.CharField(widget=forms.Textarea(attrs={'class':'wysiwyg', 'cols':'75', 'rows':'20'}))

    tags = forms.CharField(initial='', required=False,
                           widget=forms.TextInput(attrs={'size': 100}),
                           help_text=_('Words that describe this article'))

    def __init__(self, *args, **kwargs):
        """Sets the list of tags to be a string"""

        instance = kwargs.get('instance', None)
        if instance:
            init = kwargs.get('initial', {})
            init['tags'] = ', '.join([t.name for t in instance.tags.all()])
            kwargs['initial'] = init

        super(PostAdminForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):

        if self.cleaned_data['tags']:
            tag = lambda n: Tag.objects.get_or_create(slug=slugify(n.strip()), name=n)[0]
            tags = [tag(t) for t in self.cleaned_data['tags'].split(',')]
            self.cleaned_data['tags'] = tags
        else:
            self.cleaned_data['tags'] = []

        return super(PostAdminForm, self).save(*args, **kwargs)

    '''
    def __clean_tags(self):
        """Turns the string of tags into a list"""
        tag = lambda n: Tag.objects.get_or_create(slug=Tag.clean_tag(n), name=n)[0]
        tags = [tag(t) for t in self.cleaned_data['tags'].split()]
        self.cleaned_data['tags'] = tags
        return self.cleaned_data['tags']
    '''

    class Meta:
        model = Post

    class Media:
        css = {
            'all': ('css/jquery.autocomplete.css',),
        }
        js = (
            'js/jquery-1.4.2.min.js',
            'js/jquery.bgiframe.min.js',
            'js/jquery.autocomplete.pack.js',
            'js/tag_autocomplete.js',
        )

