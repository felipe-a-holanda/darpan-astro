from django.db import models
from django.conf import settings

from django.utils.translation import ugettext_lazy as _

from timezone_field import TimeZoneField
import datetime
import pytz


class Chart(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='chart', on_delete=models.CASCADE)
    
    name = models.CharField(_('full name'), max_length=255, default='', blank=True)
    
    #local time:
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True)
    
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    
    timezone = TimeZoneField(blank=True)
    
    #utc time:
    datetime_utc = models.DateTimeField(null=True, blank=True)
    
    
    def convert_timezone(self):
        if self.date:
            if self.time and self.timezone:
                datetime_utc = datetime.datetime.combine(self.date, self.time)
                local_moment = self.timezone.localize(datetime_utc)
                
            else:
                datetime_utc = datetime.datetime.combine(self.birthdate, datetime.time(12,0))
                local_moment = pytz.utc.localize(datetime_utc)
            
            
            utc_moment = local_moment.astimezone(pytz.utc)
            self.datetime_utc = utc_moment
        
    
    def save(self, *args, **kwargs):
        self.convert_timezone()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
