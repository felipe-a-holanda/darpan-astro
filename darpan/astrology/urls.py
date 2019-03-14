from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from .views import *


app_name = 'astrology'

urlpatterns = [
    path('', AstroListView.as_view(), name='list'),
    path('chart/<str:username>/<int:pk>', AstroDetailView.as_view(), name='detail'),
    path('planet/<str:planet>/<str:sign>', AstroPlanetSign.as_view(), name='planetsign'),
]
