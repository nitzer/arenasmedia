from django.conf.urls.defaults import *
from django.contrib import admin
from apps.djblog import urls as djblog_urls
from django.views.generic.simple import direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'base.html'}),
    (r'^blog/', include(djblog_urls.blog())),
   
    #(r'^app/', include('apps.djanswer.urls')),
    (r'^users/', include('apps.user_profile.urls')),
    (r'^admin/', include(admin.site.urls)),

    # registration
    (r'^accounts/', include('apps.registration.backends.default.urls')),

    # contact
    (r'^contact/$', include('apps.djcontact.urls')),
    (r'^contact/sent/$' , 'djcontact.views.contact_form', {'template_name':'djcontact/contact_form_sent.html'} ),

    (r'^captcha/', include('apps.captcha.urls')),

    #subscribe
    (r'^djsubscribe/$', include('apps.djsubscribe.urls')),
	( r'^djsubscribe/pre/$' , direct_to_template , {'template': 'djsubscribe/subscribe_pre.html'} ),
    ( r'^djsubscribe/sent/$' , 'djsubscribe.views.subscribe_form' , {'template_name':'djsubscribe/subscribe_sent.html'} ),

    # feeds
    (r'^feeds/', include(djblog_urls.feed())),

    # by special (no blog) category
    (r'', include(djblog_urls.noblog())),

)

import sys, os
from django.conf import settings
if 'runserver' in sys.argv or 'runserver_plus':
    urlpatterns = patterns('', url(r'^media/(.*)$', 'django.views.static.serve', 
        kwargs={'document_root': settings.MEDIA_ROOT}), 
    ) + urlpatterns
