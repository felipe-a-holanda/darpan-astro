
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from .views import *


app_name = 'hds'

urlpatterns = [
    path('', RaveChartListView.as_view(), name='list'),
    path('chart/<str:username>/<int:pk>', RaveChartDetailView.as_view(), name='detail'),
    path('gate/<str:slug>', GateDetailView.as_view(), name='gate-detail'),
    path('center/<str:slug>', CenterDetailView.as_view(), name='center-detail'),
    path('channel/<str:slug>', ChannelDetailView.as_view(), name='channel-detail'),
]
