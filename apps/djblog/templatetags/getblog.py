# *-* coding=utf-8 *-*

"""
Templatetags básicos para traer posts, tags y blocks
"""

from django import template
from djblog.models import Post, Tag, Category
from django.db.models import Count, Q
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

register = template.Library()

class CommonNode(template.Node):
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
            if type(v) is int or v is None:
                setattr(self, k+'_template', v)
            else:
                setattr(self, k+'_template', template.Variable(v))



class BlogTagsNode(CommonNode):
    def render(self, context):
        qs = Tag.objects.all().annotate(weight=Count('post'))
        if self.var:
            try:
                var = self.var_template.resolve(context)
            except template.VariableDoesNotExist:
                var = self.var

            context[var] = qs
            return ''

        return qs

""" obtiene los tags del blog """
def get_blog_tags(parse, token):
    """ {% get_blog_tags as tags %} """
    var = None
    stk = token.split_contents()
    try:
        tag, _as, var = stk
    except:
        pass

    return BlogTagsNode(var=var)



class BlogCategoriesNode(CommonNode):
    def render(self, context):
        qs = Category.objects.blog().filter(root_level__lte=0)
        if self.var:
            try:
                var = self.var_template.resolve(context)
            except template.VariableDoesNotExist:
                var = self.var

            context[var] = qs
            return ''

        return qs

""" obtiene las categoías del blog """
def get_blog_categories(parse, token):
    var = None
    stk = token.split_contents()
    try:
        tag, _as, var = stk
    except:
        pass

    return BlogCategoriesNode(var=var)



class LatestBlogPostsNode(CommonNode):
    def render(self, context):
        qs = Post.objects.get_blog_posts()
        if self.var:
            try:
                var = self.var_template.resolve(context)
            except template.VariableDoesNotExist:
                var = self.var

            context[var] = qs
            return ''

        return qs

""" obtiene los últimos posts del blog """
def get_latest_blog_posts(parse, token):
    """
    {% get_latest_blog_posts as posts %}
    {% with posts|first as post %}
    """
    var = None
    stk = token.split_contents()
    try:
        tag, _as, var = stk
    except:
        pass

    return LatestBlogPostsNode(var=var)



class LatestCategoryPostsNode(template.Node):
    def __init__(self, var=None, cat=[], ncat=[], recursive=False):

        setattr(self, 'var', var)
        setattr(self, 'recursive', recursive)

        _cat = []
        for k,v in enumerate(cat):
            if '.' in v:
                nvar = 'cat'+str(k)+'_template'
                setattr(self, nvar, template.Variable(v))
            else:
                nvar = 'cat'+str(k)+'_str'
                setattr(self, nvar, v)
            _cat.append(nvar)
        setattr(self, 'cat', _cat)

        _cat = []
        for k,v in enumerate(ncat):
            if '.' in v:
                nvar = 'ncat'+str(k)+'_template'
                setattr(self, nvar, template.Variable(v.replace('!','')))
            else:
                nvar = 'ncat'+str(k)+'_str'
                setattr(self, nvar, v)
            _cat.append(nvar)
        setattr(self, 'ncat', _cat)

    def render(self, context):
        qs = Post.objects.get_posts()
        # filtramos por las categorias que si se incluyen
        if self.cat:
            cats = []
            for c in self.cat:
                cat = getattr(self, c)
                try:
                    cat = cat.resolve(context)
                    cat = cat.slug
                except:
                    pass
                cats.append(cat)
           
            #print 'in category', cats
            if self.recursive:
                qs = qs.filter(Q(category__slug__in=cats) | Q(category__parent__slug__in=cats))
            else:
                qs = qs.filter(category__slug__in=cats)

        #print qs
        # filtramos por las categorias que no se incluyen
        if self.ncat:
            cats = []
            for c in self.ncat:                
                cat = getattr(self, c)
                try:
                    cat = cat.resolve(context)
                    cat = cat.slug
                except:
                    pass
                cats.append(cat)

            #print 'not in category', cats
            if self.recursive:
                qs = qs.exclude(Q(category__slug__in=cats) | Q(category__parent__slug__in=cats))
            else:
                qs = qs.exclude(category__slug__in=cats)

        if self.var:
            try:
                var = self.var.resolve(context)
            except:
                var = self.var

            context[var] = qs
            return ''

        return qs

""" obtiene los posts de una o varias categorías, de blog o noblog """
def get_latest_category_posts(parse, token):
    """
    {% get_latest_category_posts category:!notcategory:object.category norecursive as posts %}
    {% with posts|first as post %}
    """
    var = None
    cat = []
    ncat = []
    _cat = None
    stk = token.split_contents()
    try:
        tag, _cat, _recursive, _as, var = stk
    except:
        try:
            tag, _cat, _recursive = stk
        except:
            pass
    for c in _cat.split(':'):
        if '!' in c:
            ncat.append(c)
        else:
            cat.append(c)

    _recursive = _recursive == u'recursive'

    return LatestCategoryPostsNode(var=var, cat=cat, ncat=ncat, recursive=_recursive)


register.tag(get_latest_category_posts)
register.tag(get_latest_blog_posts)
register.tag(get_blog_categories)
register.tag(get_blog_tags)
