from django.db import models
from django import forms
from django.utils.translation import ugettext_lazy as _

# Create your models here.

attrs_dict = { 'class': 'required' }

class Subscribe(models.Model):
	email = models.EmailField()
	def __unicode__(self):
		return str(self.email)
	class Meta:
		ordering = ["id"]
		verbose_name_plural = "Subscriptos"
