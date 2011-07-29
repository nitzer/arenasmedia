from django import template
from apps.djsubscribe.forms import SubscribeForm
register = template.Library()

@register.inclusion_tag('djsubscribe/subscribe_form.html')
def get_subscribe_form():
    return {'form': SubscribeForm()}
