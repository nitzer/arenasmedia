from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
    ( r'' , 'djsubscribe.views.subscribe_form' ),
	( r'^djsubscribe/pre/$' , direct_to_template , {'template': 'djsuscribe/subscribe_pre.html'} ),
    ( r'^djsubscribe/sent/$' , 'djsubscribe.views.subscribe_form' , {'template_name':'djsubscribe/subscribe_sent.html'} ),
#	( r'pre/', direct_to_template, {'template': 'djsuscribe/subscribe_pre.html'}, name='djsubscribe'),
)
