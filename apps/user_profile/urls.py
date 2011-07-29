from django.conf.urls.defaults import *

urlpatterns = patterns('user_profile.views',
    url(r'(?P<username>[a-zA-Z0-9\-\_\.\@]+)/$', 'profile', name="user_profile"),
    #(r'profile/', ''),
    
)
