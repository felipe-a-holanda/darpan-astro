from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from charts.models import Chart

import swisseph as swe
from jsonfield import JSONField

from .astrolib import Planet, SIGN_INDEX_DIC
from .astrolib import AstroChart as AstroChart_

class AstroChartQuerySet(models.QuerySet):
    def planet_sign(self, planet, sign):
        planet=planet.lower()
        sign_index = SIGN_INDEX_DIC[sign]

        gt = sign_index*30
        lt = (sign_index+1)*30
        kwargs = {'{0}__lt'.format(planet):lt, '{0}__gt'.format(planet):gt}
        return self.filter(**kwargs)


class AstroChart(models.Model):
    chart = models.OneToOneField(Chart, related_name='astrochart', on_delete=models.CASCADE)
    
    sun = models.FloatField()
    moon = models.FloatField()
    mercury = models.FloatField()
    venus = models.FloatField()
    mars = models.FloatField()
    jupiter = models.FloatField()
    saturn = models.FloatField()
    uranus = models.FloatField()
    neptune = models.FloatField()
    pluto = models.FloatField()
    
    #sinastry_points = models.CharField(max_length=200*30, blank=True, null=True)
    sinastry_points =  JSONField(null=True, blank=True)

    objects = AstroChartQuerySet.as_manager()


    def __str__(self):
        return str(self.chart)

    def planet(self, index):
        return Planet(index, self)

    def planets(self):
        planets = []
        for i in range(swe.NPLANETS):
            p = Planet(i, self)
            if hasattr(p, 'angle'):
                planets.append(p)
        return planets


    def save(self, *args, **kwargs):
        #self.datetime_utc = self.chart.datetime_utc
        #self.latitude = self.city.latitude
        #self.longitude = self.city.longitude
        self.calculate_chart()
        super().save(*args, **kwargs)

    def julday(self):
        d = self.chart.datetime_utc
        return swe.julday(d.year, d.month, d.day, d.hour+d.minute/60.0)

    def calculate_chart(self):
        julday = self.julday()
        self.sun = swe.calc_ut(julday, 0)[0]
        self.moon = swe.calc_ut(julday, 1)[0]
        self.mercury = swe.calc_ut(julday, 2)[0]
        self.venus = swe.calc_ut(julday, 3)[0]
        self.mars = swe.calc_ut(julday, 4)[0]
        self.jupiter = swe.calc_ut(julday, 5)[0]
        self.saturn = swe.calc_ut(julday, 6)[0]
        self.uranus = swe.calc_ut(julday, 7)[0]
        self.neptune = swe.calc_ut(julday, 8)[0]
        self.pluto = swe.calc_ut(julday, 9)[0]
        
        #self.sinastry_points = self.generate_sinastry_model()
    
    
    def calc_astrochart(self):
        date = self.chart.datetime_utc
        if self.chart.city:
            lat = self.chart.city.latitude
            lon = self.chart.city.longitude
            
            return AstroChart_(date, lat, lon)
        #return None
        return AstroChart_(date, None, None)
        
    def generate_sinastry_model(self, interactions=1000):
        return self.calc_astrochart().generate_sinastry_model(interactions)
        
    def sinastry(self, other):
        chart1 = self.calc_astrochart()
        chart2 = other.calc_astrochart()
        aspects, points, abs_points = chart1.calc_sinastry(chart2)
        points
        if points < 0:
            return points, self.sinastry_points[0]
        return points, self.sinastry_points[points]
        
    def compatibility(self):
        owner_chart = self.chart.owner.profile.chart.astrochart
        return owner_chart.sinastry(self)
        
        
        

@receiver(post_save, sender=Chart)
def create_astrochart(sender, **kwargs):
    chart = kwargs["instance"]
    if kwargs["created"]:
        astrochart = AstroChart(chart=chart)
        astrochart.save()
    else:
        chart.astrochart.save()
