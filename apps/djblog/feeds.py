# *-* coding=utf-8 *-*

from django.conf.urls.defaults import *
from django.conf import settings
#from django.contrib.syndication.feeds import Feed
from django.contrib.syndication.views import Feed
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.core.urlresolvers import reverse
from djblog.models import Post, Tag

SITE = Site.objects.get_current()

# default to 24 hours for feed caching
DJBLOG_FEED_TIMEOUT = getattr(settings, 'DJBLOG_FEED_TIMEOUT', 86400)


class LatestFeed(Feed):
    def title(self):
        return "%s Posts" % SITE.name

    def link(self):
        return reverse('djblog_latest')

    def items(self):
        key = 'djblog_feed_latest'
        qs = cache.get(key)

        if qs is None:
            qs = list(Post.objects.get_posts().filter(lang__iexact=settings.LANGUAGE_CODE).order_by('-publication_date')[:15])
            cache.set(key, qs, DJBLOG_FEED_TIMEOUT)

        return qs

    def item_link(self, obj):
        return obj.get_absolute_url() #reverse('djblog_latest')

    def item_author_name(self, item):
        return item.author.username

    def item_tags(self, item):
        return [c.name for c in item.tags.all()] + [keyword.strip() for keyword in item.keywords.split(',')]

    def item_pubdate(self, item):
        return item.publication_date



class CategoryFeed(Feed):
    pass

class TagFeed(Feed):
    pass

class AuthorFeed(Feed):
    pass

urlpatterns = patterns('',
    # latest feed
    url('^$', LatestFeed(), name='djblog_feed'),

    # feed by category
    url(r'^category/(?P<category>[a-zA-Z0-9\-\_\.\/]+)$', CategoryFeed(), name='djblog_feed_category'),

    # feed by tag
    url(r'^tag/(?P<tag>[a-zA-Z0-9\-\_\.]+)$', TagFeed(), name='djblog_feed_tag'),

    # feed by author
    url(r'^author/(?P<username>[a-zA-Z0-9\-\_\.]+)$', AuthorFeed(), name='djblog_feed_author'),

)
