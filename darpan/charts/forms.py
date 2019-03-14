import re

from django import forms
from django.forms.models import modelformset_factory, formset_factory
from .models import Chart

class ChartForm(forms.ModelForm):
    class Meta:
        model = Chart
        fields = ('name', 'date', 'time', 'timezone', 'country', 'city')


class ImportChartForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)

    


ChartFormSet = formset_factory(form=ChartForm, extra=1, max_num=20)




class ContactForm1(forms.Form):
    subject = forms.CharField(max_length=100)
    sender = forms.EmailField()

class ContactForm2(forms.Form):
    message = forms.CharField(widget=forms.Textarea)
