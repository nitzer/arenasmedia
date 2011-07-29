from models import Subscribe
from django.forms import ModelForm


attrs_dict = { 'class': 'required' }

class SubscribeForm(ModelForm):
	class Meta:
		model = Subscribe


