from django.urls import path, include

from .views import *

app_name = 'cities'

urlpatterns = [
    path(
        'country-autocomplete/',
        CountryAutocomplete.as_view(),
        name='country-autocomplete',
    ),

    path(
        'city-autocomplete/',
        CityAutocomplete.as_view(),
        name='city-autocomplete',
    ),

    path(
        'timezone-autocomplete/',
        TimezoneAutocomplete.as_view(),
        name='timezone-autocomplete',
    ),

]
