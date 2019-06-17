from django.db import models
from django.conf import settings
from django.urls import reverse

from django.utils.translation import ugettext_lazy as _

from django.db.models.signals import post_save, pre_save
from django.db.models import signals
from django.dispatch import receiver

from timezone_field import TimeZoneField
import datetime
import pytz

from autoslug import AutoSlugField
from cities.models import City, Country


class Chart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='charts', on_delete=models.CASCADE)

    name = models.CharField(_('full name'), max_length=255, default='', blank=True)

    slug = AutoSlugField(populate_from='name', always_update=True, unique_with=('owner'))

    #local time:
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)


    country = models.ForeignKey(Country ,  blank=True, null=True, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, blank=True, null=True, on_delete=models.SET_NULL)

    timezone = TimeZoneField(blank=True)

    #utc time:
    datetime_utc = models.DateTimeField(null=True, blank=True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('chart:detail', kwargs={'username':self.owner.username, 'pk': self.pk})





def calculate_utc_time(chart):
    if chart.date:
        if chart.time and chart.timezone:
            datetime_utc = datetime.datetime.combine(chart.date, chart.time)
            local_moment = chart.timezone.localize(datetime_utc)

        else:
            datetime_utc = datetime.datetime.combine(chart.date, datetime.time(12,0))
            local_moment = pytz.utc.localize(datetime_utc)


        utc_moment = local_moment.astimezone(pytz.utc)
        chart.datetime_utc = utc_moment

@receiver(pre_save, sender=Chart)
def populate_timezone_from_city(sender, **kwargs):
    chart = kwargs["instance"]
    if chart.city:
        chart.timezone = chart.city.timezone
        chart.country = chart.city.country

    calculate_utc_time(chart)

    signals.pre_save.disconnect(populate_timezone_from_city, sender=Chart)
    chart.save()
    signals.pre_save.connect(populate_timezone_from_city, sender=Chart)
