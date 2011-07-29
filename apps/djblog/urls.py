# *-* coding=utf-8 *-*

from django.conf.urls.defaults import *

def blog():

    # urls de blog
    urlpatterns = patterns('djblog.views',
        # by date
        url(r'^(?P<year>\d{4})/(?P<month>\d{1,3})/(?P<day>\d{1,2})/(?P<slug>[a-zA-Z0-9\-\_\.]+)/$', 'postdate', name='djblog_postdate'),

        # by category
        url(r'^category/(?P<category>[a-zA-Z0-9\-\_\.\/]+)$', 'category', name='djblog_category'),

        # by tag
        url(r'^tag/(?P<tag>[a-zA-Z0-9\-\_\.]+)$', 'tag', name='djblog_tag'),

        # by author
        url(r'^author/(?P<username>[a-zA-Z0-9\-\_\.]+)$', 'author', name='djblog_author'),

        # search
        url(r'^search/$', 'search', name='djblog_search'),

        # AJAX
        url(r'^ajax/tag/autocomplete/$', 'ajax_tag_autocomplete', name='djblog_tag_autocomplete'),

        # latest
        url(r'^$', 'latest', name='djblog_latest'),
    )

    return urlpatterns

def noblog():
    
    # urls no blog
    urlpatterns = patterns('djblog.views',
        # by slug (pages)
        url(r'^page/(?P<slug>[a-zA-Z0-9\-\_\.]+)/$', 'page', name='djblog_page'),

        # by special (no blog) category
        url(r'^(?P<category>[a-zA-Z0-9\-\_\.]+)/post/(?P<slug>[a-zA-Z0-9\-\_\.]+)/$', 'noblog_post', name='djblog_noblog_post'),
        url(r'^(?P<category>[a-zA-Z0-9\-\_\.\/]+)/$', 'noblog_category', name='djblog_noblog_category'),


    )

    return urlpatterns


def feed():

    # urls de feed
    urlpatterns = patterns('djblog.feeds',
        # latest feed
        url('^latest/$', include('djblog.feeds')),
    )

    return urlpatterns

urlpatterns = blog() + noblog() + feed()
