from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from charts.models import Chart

import swisseph as swe

from .astrolib import Planet



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

@receiver(post_save, sender=Chart)
def create_astrochart(sender, **kwargs):
    chart = kwargs["instance"]
    if kwargs["created"]:
        astrochart = AstroChart(chart=chart)
        astrochart.save()
    else:
        chart.astrochart.save()
