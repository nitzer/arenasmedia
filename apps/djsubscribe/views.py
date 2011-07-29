from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from django.core.mail import send_mail
from forms import SubscribeForm


def subscribe_form(request, form_class=SubscribeForm,
                 template_name='djsubscribe/subscribe.html',
                 success_url=None, 
				 extra_context=None,
                 fail_silently=False):
	if request.method == 'POST':
		form = SubscribeForm(request.POST)
		if form.is_valid():
			form.save()
			send_mail(
				'Subscripcion de %s a %s' % (request.POST['email'],request.POST['email']) , ' Nombres:%s\n Email: %s\n Empresa: %s\n Categoria: %s\n ' %(request.POST['nombres'],request.POST['email'],request.POST['empresa'],request.POST['categoria']) , request.POST['email'] ,
				settings.DJSUBSCRIBE_TO_EMAIL, fail_silently=False)
			if success_url :
				return HttpResponseRedirect(success_url)
			else:
				return HttpResponseRedirect('/djsubscribe/sent/')
	else :
		form = SubscribeForm()

	if extra_context is None:
		extra_context = {}
	context = RequestContext(request)
	for key, value in extra_context.items():
		context[key] = callable(value) and value() or value
	return render_to_response(template_name,
                              { 'form': form },
                              context_instance=context)
