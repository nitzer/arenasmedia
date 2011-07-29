# *-* coding=utf-8 *-*

from django.http import HttpResponse
from django.views.generic import list_detail, create_update, simple, date_based
from django.shortcuts import get_object_or_404
from django.conf import settings
from djblog.models import Post, Tag, Category
from django.db.models import Q
from django.template.loader import select_template

DJBLOG_PAGINATION = getattr(settings, 'DJBLOG_PAGINATION', 5)

def _get_template(temps):
    return select_template(temps).name

def _resolve_lang(request, qs):
    if 'l' in request.GET and request.GET['l']:
        qs = qs.filter(Q(lang__iexact=request.GET['l']) | Q(lang__istartswith=request.GET['l']))
        if qs:
            return qs
    return qs.filter(lang__iexact=settings.LANGUAGE_CODE)

""" view for object_lists """

""" for blog """

def latest(request):
    # últimos posts
    extra_context = {'djblog_in': 'Latest'}
    qs = Post.objects.get_blog_posts()
    qs = _resolve_lang(request, qs)
    return list_detail.object_list(request, queryset=qs, paginate_by=DJBLOG_PAGINATION, extra_context=extra_context)


def category(request, category=None):
    # posts de una categoría
    category = category.split('/')[-1]
    category = get_object_or_404(Category.objects.blog(), slug=category)
    qs = Post.objects.get_blog_posts().filter(Q(category__in=[category]) | Q(category__parent__in=[category]))
    qs = _resolve_lang(request, qs)

    extra_context = {'category': category, 'djblog_in': 'Category'}
    category = category.get_root_category()
    template = _get_template(['djblog/%s/post_list.html' % category.slug, 'djblog/post_list.html'])
    return list_detail.object_list(request, template_name=template, queryset=qs, paginate_by=DJBLOG_PAGINATION, extra_context=extra_context)


def tag(request, tag=None):
    # posts asociados de un tags
    extra_context = {'djblog_in': 'Tag'}
    qs = Post.objects.get_posts().filter(tags__slug=tag)
    qs = _resolve_lang(request, qs)
    return list_detail.object_list(request, queryset=qs, paginate_by=DJBLOG_PAGINATION, extra_context=extra_context)


def author(request, username=None):
    # posts de autor
    extra_context = {'djblog_in': 'Author'}
    qs = Post.objects.get_blog_posts().filter(author__username=username)
    qs = _resolve_lang(request, qs)

    return list_detail.object_list(request, queryset=qs, paginate_by=DJBLOG_PAGINATION, extra_context=extra_context)


def search(request):
    # busca entre opsts, por contenido, título y copete
    extra_context = {'djblog_in': 'Search'}
    qs = Post.objects.get_posts()
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        qs = qs.filter(Q(content_plain__icontains=q) | Q(title__icontains=q) | Q(copete__icontains=q))
        extra_context.update({'search_q': q})
        if 'c' in request.GET and request.GET['c']:
            c = request.GET['c']
            qs = qs.filter(category__slug=c)
    qs = _resolve_lang(request, qs)
    return list_detail.object_list(request, queryset=qs, paginate_by=DJBLOG_PAGINATION, extra_context=extra_context)



""" for noblog """

def noblog_category(request, category=None):
    # posts o páginas de una categoía (noblog)
    category = category.split('/')[-1]
    qs = Post.objects.get_noblog_posts().filter(Q(category__slug__in=[category]) | Q(category__parent__slug__in=[category]))
    qs = _resolve_lang(request, qs)

    category = get_object_or_404(Category, slug=category).get_root_category()

    extra_context = {'category': category, 'djblog_in': 'Category'}
    template = _get_template(['djblog/%s/post_list.html' % category.slug, 'djblog/post_list.html'])
    return list_detail.object_list(request, template_name=template, queryset=qs, paginate_by=DJBLOG_PAGINATION, extra_context=extra_context)





""" views for object_detail """

""" for blog """

def postdate(request, year=None, month=None, day=None, slug=None):
    # muestra un post, por su fecha y slug
    extra_context = {}
    qs = Post.objects.get_blog_posts()
    qs = _resolve_lang(request, qs)

    return date_based.object_detail(request, queryset=qs, year=year, month=month, day=day, slug=slug, 
            date_field='publication_date', month_format='%m', extra_context=extra_context)



""" for noblog """

def noblog_post(request, category=None, slug=None):
    # muestra un post por su categoría (noblog) y slug
    category = category.split('/')[-1]
    #qs=Post.objects.get_noblog_posts().filter(category__slug=category)
    qs = Post.objects.get_noblog_posts().filter(Q(category__slug__in=[category]) | Q(category__parent__slug__in=[category]))
    qs = _resolve_lang(request, qs)

    category = get_object_or_404(Category, slug=category).get_root_category()

    extra_context = {'category': category, 'djblog_in': 'Category'}
    template = _get_template(['djblog/%s/post_detail.html' % category.slug, 'djblog/post_detail.html'])
    return list_detail.object_detail(request, template_name=template, queryset=qs, slug=slug, extra_context=extra_context)


def page(request, slug=None):
    # muestra una página por su slug
    qs = Post.objects.get_pages()
    qs = _resolve_lang(request, qs)

    category = get_object_or_404(qs, slug=slug).get_root_category()

    templates = ['djblog/page_%s.html' % slug, 'djblog/page_detail.html']
    if category:
        templates.insert(0, 'djblog/%s/page_detail.html' % category.slug)
        templates.insert(0, 'djblog/%s/page_%s.html' % (category.slug, slug))

    extra_context = {'category': category, 'djblog_in': 'Category'}
    template = _get_template(templates)
    #print qs, slug, template
    return list_detail.object_detail(request, template_name=template, queryset=qs, slug=slug, extra_context=extra_context)


def ajax_tag_autocomplete(request):
    if 'q' in request.GET:
        q = request.GET['q']
        tags = list(Tag.objects.filter(name__istartswith=q)[:10])
        response = HttpResponse(u'\n'.join(tag.name for tag in tags))
        return response

    return HttpResponse()
