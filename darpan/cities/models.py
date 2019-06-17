import cities_light
import pytz

from django.db import models
from timezone_field import TimeZoneField

from cities_light.settings import ICity
from cities_light.receivers import connect_default_signals
from cities_light.abstract_models import (AbstractCountry, AbstractRegion, AbstractCity)


class Country(AbstractCountry):
    pass
connect_default_signals(Country)


class Region(AbstractRegion):
    pass
connect_default_signals(Region)


class City(AbstractCity):
    timezone = TimeZoneField(null=True)
connect_default_signals(City)


def process_city_import(sender, instance, items, **kwargs):
    instance.timezone = pytz.timezone(items[ICity.timezone])


cities_light.signals.city_items_post_import.connect(process_city_import)
