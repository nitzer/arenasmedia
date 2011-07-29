# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.conf import settings
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

try:
    USER_THUMBNAIL_SIZE = settings.USER_THUMBNAIL_SIZE
except:
    USER_THUMBNAIL_SIZE = (75,75)

class UserProfile(models.Model):
    AGE_RANGE = (
        ('18-25', '18-25'),
        ('25-35', '25-35'),
        ('35-50', '35-50'),
        ('50-65', '50-65'),
        ('mayor de 65', 'mayor de 65'),
    )

    GENDER = (
        ('F', 'Femenino'),
        ('M', 'Masculino'),
        ('X', 'Prefiero no revelar'),
    )

    def thumbpath(self, filename, *args, **kwargs):
        return 'users/thumb/%s_%s' % (self.username, filename)

    user = models.ForeignKey(User, editable=False, verbose_name=_(u"Nombre de usuario"))
    country = models.CharField(max_length=150, blank=True, verbose_name=_(u"Ubicación"), help_text=_(u"ej.: Buenos Aires, Argentina"))
    thumb = models.ImageField(upload_to=thumbpath, blank=True, verbose_name=_(u"Avatar"))
    age_range = models.CharField(max_length=30, choices=AGE_RANGE, blank=True, verbose_name=_(u"Edad"))
    gender = models.CharField(max_length=1, choices=GENDER, blank=True, verbose_name=_(u"Género"))

    #información del usuario opcional
    web = models.URLField(blank=True, verbose_name=_(u"Web"), help_text="Página web o blog")
    date_of_birth = models.DateField(blank=True, null=True, verbose_name="Fecha de Nacimiento", help_text="Formato dd/mm/aaaa")
    biography = models.CharField(blank=True, max_length=500, verbose_name=_(u"Mis intereses o Biografía"), help_text="Máximo 500 caracteres.")


    #custom username property, extiende desde User
    def _get_username(self): return self.user.username
    def _set_username(self, value): 
        self.user.username = value
    username = property(_get_username, _set_username)

    #custom first_name property, extiende desde User
    def _get_first_name(self): return self.user.first_name
    def _set_first_name(self, value): 
        self.user.first_name = value
    first_name = property(_get_first_name, _set_first_name)

    #custom last_name property, extiende desde User
    def _get_last_name(self): return self.user.last_name
    def _set_last_name(self, value): 
        self.user.last_name = value
    last_name = property(_get_last_name, _set_last_name)

    #custom email property, extiende desde User
    def _get_email(self): return self.user.email
    def _set_email(self, value): self.user.email = value
    email = property(_get_email, _set_email)

    #obtiene el nombre real, si lo tiene sino decuelve el username
    def _get_fullname(self): return (lambda x,y,z: z or (x +' '+ y))(self.first_name, self.last_name, self.username)
    fullname = property(_get_fullname)

    def _get_profile(self):
        return (
                ('username', u"Nombre de usuario", self.username),
                ('first_name', u"Nombre(s)", self.first_name),
                ('last_name', u"Apellido(s)", self.last_name),
                ('email', u"Email", self.email),
                ('country', u"Ubicación", self.country),
                ('age_range', u"Edad", self.get_age_range_display()),
                ('gender', u"Genero", self.get_gender_display()),
                ('web', u"Web", self.web),
                ('date_of_birth', u"Fecha de nacimiento", self.date_of_birth),
                ('biography', u"Mis intereses/Biografía", self.biography),
        )
    profile = property(_get_profile)

    def __unicode__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        super(UserProfile, self).save(*args, **kwargs)
        if self.thumb:
            from PIL import Image
            import os
 
            img_path = os.path.join(settings.MEDIA_ROOT, self.thumb.path)
            image = Image.open(img_path)
        
            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')
        
            image.thumbnail(USER_THUMBNAIL_SIZE, Image.ANTIALIAS)
            image.save(os.path.join(settings.MEDIA_ROOT, self.thumb.path))

        super(UserProfile, self).save(*args, **kwargs)
        super(User, self.user).save()

    class Meta:
        verbose_name = _("Profiles")
        verbose_name_plural = _("Profiles")
        #app_label = "profiles"
        #db_table = 'user_profile_userprofile'

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            profile = UserProfile.objects.get(user=instance)
        except UserProfile.DoesNotExist:
            profile, created = UserProfile.objects.get_or_create(user=instance)
post_save.connect(create_user_profile, sender=User)
