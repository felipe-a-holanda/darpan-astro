"""darpan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic.base import TemplateView
from .views import *


app_name = 'charts'

urlpatterns = [
    path('', ChartListView.as_view(), name='list'),
    path('new', ChartCreateView.as_view(), name='new'),
    path('import', ChartImportView.as_view(), name='import'),
    path('import2', MultipleChartCreate.as_view(), name='import2'),
    path('wizard', ContactWizard.as_view(), name='wizard'),

    path('<str:username>/<int:pk>', ChartDetailView.as_view(), name='detail'),

    #path('post/create/', PostCreate.as_view(), name='post_create'),
    #path('chart/<str:pk>', NumerologyDetailView.as_view()),
    #path('<str:tag>', PostListFormView.as_view(), name='posts'),
    #path('<str:tag>/<str:tag2>', PostListFormView.as_view(), name='posts'),
]
