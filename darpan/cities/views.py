from django.shortcuts import render

# Create your views here.
from dal import autocomplete

from .models import Country, City
import pytz


class CountryAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Country.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs


class TimezoneAutocomplete(autocomplete.Select2ListView):
    def get_list(self):
        return pytz.all_timezones


class CityAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = City.objects.all()

        country = self.forwarded.get('country', None)
        if country:
            print(country)
            qs = qs.filter(country__id=country)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs

    def get_result_label(self, item):
        return "%s, %s" % (item.name, item.region.name)
