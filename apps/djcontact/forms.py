from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from django.template import RequestContext
from django.contrib.sites.models import Site
from apps.captcha.fields import CaptchaField
from django.utils.translation import ugettext_lazy as _

attrs_dict = { 'class': 'required' }

class ContactForm(forms.Form):

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=_(u'Nombre(s) y Apellido(s)'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=200)), label=_(u'Email'))
    telephone = forms.CharField(max_length=100, widget=forms.TextInput(attrs=attrs_dict), label=_(u'Tel&eacute;fono'))
    body = forms.CharField(widget=forms.Textarea(attrs=attrs_dict), label=_(u'Mensaje'))
    
    captcha = CaptchaField(label=_(u'Seguridad'))

    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [mail_tuple[1] for mail_tuple in settings.MANAGERS]
    subject_template_name = "djcontact/contact_form_subject.txt"
    template_name = 'djcontact/contact_form.txt'


    def __init__(self, data=None, files=None, request=None, *args, **kwargs):
        if request is None:
            raise TypeError("Keyword argument 'request' must be supplied")
        super(ContactForm, self).__init__(data=data, files=files, *args, **kwargs)
        self.request = request


    def message(self):
        """
        Render the body of the message to a string.
        
        """
        if callable(self.template_name):
            template_name = self.template_name()
        else:
            template_name = self.template_name
        return loader.render_to_string(template_name,
                                       self.get_context())
    
    def subject(self):
        """
        Render the subject of the message to a string.
        
        """
        subject = loader.render_to_string(self.subject_template_name,
                                          self.get_context())
        return ''.join(subject.splitlines())
    
    def get_context(self):
        """
        Return the context used to render the templates for the email
        subject and body.

        By default, this context includes:

        * All of the validated values in the form, as variables of the
          same names as their fields.

        * The current ``Site`` object, as the variable ``site``.

        * Any additional variables added by context processors (this
          will be a ``RequestContext``).
        
        """
        if not self.is_valid():
            raise ValueError("Cannot generate Context from invalid contact form")
        return RequestContext(self.request,
                              dict(self.cleaned_data,
                                   site=Site.objects.get_current()))
    
    def get_message_dict(self):
        """
        Generate the various parts of the message and return them in a
        dictionary, suitable for passing directly as keyword arguments
        to ``django.core.mail.send_mail()``.

        By default, the following values are returned:

        * ``from_email``

        * ``message``

        * ``recipient_list``

        * ``subject``
        
        """
        if not self.is_valid():
            raise ValueError("Message cannot be sent from invalid contact form")
        message_dict = {}
        for message_part in ('from_email', 'message', 'recipient_list', 'subject'):
            attr = getattr(self, message_part)
            message_dict[message_part] = callable(attr) and attr() or attr
        return message_dict
    
    def save(self, fail_silently=False):
        """
        Build and send the email message.
        
        """
        send_mail(fail_silently=fail_silently, **self.get_message_dict())
