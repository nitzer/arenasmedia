"""
author: Xavier Lesa <xavierlesa@gmail.com>

"""

from django.template import add_to_builtins
#add_to_builtins('socialfeed.templatetags.facebook')
#add_to_builtins('socialfeed.templatetags.twitter')
add_to_builtins('socialfeed.templatetags.getsocialfeed')
