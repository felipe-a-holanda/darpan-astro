from django.shortcuts import render
from django.views import generic
# Create your views here.

from .models import *

class RaveChartListView(generic.ListView):
    model = RaveChart

class RaveChartDetailView(generic.DetailView):
    model = RaveChart

class GateListView(generic.ListView):
    model = Gate

class GateDetailView(generic.DetailView):
    model = Gate

class ChannelListView(generic.ListView):
    model = Channel

class ChannelDetailView(generic.DetailView):
    model = Channel
    
class CenterListView(generic.ListView):
    model = Center

class CenterDetailView(generic.DetailView):
    model = Center
