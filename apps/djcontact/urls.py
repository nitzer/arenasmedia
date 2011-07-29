from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'', 'djcontact.views.contact_form', name='contact_form'),
)
