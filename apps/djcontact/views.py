from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from forms import ContactForm

def contact_form(request, form_class=ContactForm,
                 template_name='djcontact/contact_form.html',
                 success_url=None, extra_context=None,
                 fail_silently=False):

	if success_url is None:
		success_url = '/contact/sent/'
	if request.method == 'POST':
		form = form_class(data=request.POST, files=request.FILES, request=request)
		form.save(fail_silently=fail_silently)
		return HttpResponseRedirect(success_url)
# :O TODO: evitar que el captcha impida mandar el formulario.
		if form.is_valid():
			form.save(fail_silently=fail_silently)
			return HttpResponseRedirect(success_url)
	else:
		form = form_class(request=request)
    #print form
	if extra_context is None:
		extra_context = {}
	context = RequestContext(request)
	for key, value in extra_context.items():
		context[key] = callable(value) and value() or value
	return render_to_response(template_name,
								{ 'form': form },
								context_instance=context)
