from django import template
from djcontact.forms import ContactForm
register = template.Library()

@register.inclusion_tag('djcontact/contact_form.html')
def get_contact_form():
    return {'form': ContactForm()}
