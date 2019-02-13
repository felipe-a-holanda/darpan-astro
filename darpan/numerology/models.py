from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

from .numero import Numero

class NumerologyChart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='numerology_chart', on_delete=models.CASCADE)
    
    full_name = models.CharField(_('full name'), max_length=255, default='', blank=True)
    alternative_name = models.CharField(_('alternative name'), max_length=255, default='', blank=True)
    birthday = models.DateField(null=True, blank=True)
    
    life_path_number = models.PositiveSmallIntegerField(default=0, blank=True, help_text=_("From birthday"))
    destiny_number = models.PositiveSmallIntegerField(default=0, blank=True, help_text=_("From Full Name"))
    
    alternative_destiny_number = models.PositiveSmallIntegerField(default=0, blank=True, help_text=_("From Alternative Name"))
    
    def save(self, *args, **kwargs):
        numero = Numero(self.full_name, self.birthday)
        self.life_path_number = numero.get_life_path_number()
        self.destiny_number = numero.get_destiny_number()
        
        self.alternative_destiny_number = Numero(self.alternative_name).get_destiny_number()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
        
    
    def get_absolute_url(self):
        return reverse('numerology.views.numerologyDetailView', args=[str(self.id)])
