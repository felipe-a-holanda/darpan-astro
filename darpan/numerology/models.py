from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from .numero import Numero


from taggit.managers import TaggableManager

class NumerologyChart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='numerology_chart', on_delete=models.CASCADE)
    
    full_name = models.CharField(_('full name'), max_length=255, default='', blank=True)
    alternative_name = models.CharField(_('alternative name'), max_length=255, default='', blank=True)
    birthday = models.DateField(null=True, blank=True)
    
    life_path_number = models.PositiveSmallIntegerField(default=0, blank=True, help_text=_("From birthday"))
    destiny_number = models.PositiveSmallIntegerField(default=0, blank=True, help_text=_("From Full Name"))
    
    alternative_destiny_number = models.PositiveSmallIntegerField(default=0, blank=True, help_text=_("From Alternative Name"))
    
    img_url = models.URLField(null=True, blank=True)
    
    tags = TaggableManager(blank=True)
    
    def save(self, *args, **kwargs):
        numero = Numero(self.full_name, self.birthday)
        self.life_path_number = numero.get_life_path_number()
        self.destiny_number = numero.get_destiny_number()
        
        self.alternative_destiny_number = Numero(self.alternative_name).get_destiny_number()
        #self.tags.add(str(self.life_path_number), str(self.destiny_number))
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name
        
    
    def get_absolute_url(self):
        return reverse('numerology.views.numerologyDetailView', args=[str(self.id)])




@receiver(post_save, sender=NumerologyChart)    
def populate_tags(sender, **kwargs):
    chart = kwargs["instance"]
    chart.tags.add(str(chart.life_path_number), str(chart.destiny_number))
