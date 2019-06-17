import re

from django import forms
from django.forms.models import modelformset_factory, formset_factory

from dal import autocomplete

from .models import Chart

class ChartForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ChartForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['date'].required = True


    class Meta:
        model = Chart
        fields = ('name', 'date', 'time',  'country', 'city')

        widgets = {
            'timezone': autocomplete.ListSelect2(url='city:timezone-autocomplete'),
            'country': autocomplete.ListSelect2(url='city:country-autocomplete'),
            'city': autocomplete.ListSelect2(url='city:city-autocomplete', forward=('country',)),
        }


class ImportChartForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)




ChartFormSet = formset_factory(form=ChartForm, extra=1, max_num=20)
