from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.db import transaction
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# Create your views here.

from dateutil.parser import parse
from dateparser import parse

from formtools.wizard.views import SessionWizardView as WizardView

from .models import Chart
from .forms import ChartForm, ImportChartForm, ChartFormSet
from .forms import *

from cities.models import Country, City

from IPython import embed

class FormListView(FormMixin, generic.ListView):
    def get(self, request, *args, **kwargs):
        # From ProcessFormMixin
        form_class = self.get_form_class()
        self.form = self.get_form(form_class)

        # From BaseListView
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            raise Http404(_(u"Empty list and '%(class_name)s.allow_empty' is False.")
                          % {'class_name': self.__class__.__name__})

        context = self.get_context_data(object_list=self.object_list, form=self.form)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ChartListView(FormListView):
    model = Chart
    form_class = ChartForm
    
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related('city', 'owner')
        qs = qs.filter(owner=self.request.user)
        return qs

class ChartDetailView(generic.DetailView):
    model = Chart

class ChartUpdateView(generic.UpdateView):
    model = Chart
    form_class = ChartForm

class ChartCreateView(generic.CreateView):
    model = Chart
    form_class = ChartForm
    #fields = ['name', 'date', 'time', 'timezone', 'city', 'country']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)




class ContactWizard(WizardView):
    TEMPLATES = {'0': 'charts/wizard_form.html', '1':'charts/import_multiple_form.html'}

    form_list = [ImportChartForm, ChartFormSet]
    template_name = 'charts/wizard_form.html'

    def get_template_names(self):
        return [ContactWizard.TEMPLATES[self.steps.current]]


    def get_form_initial(self, step):
        #print("INITIAL",step)
        if step=='1':
            data = self.get_cleaned_data_for_step('0')['text']
            return self.process_charts(data)

        return self.initial_dict.get(step, {})

    def find_country(self, name):
        name = name.strip().lower()
        qs = Country.objects.filter(name__istartswith=name)
        if len(qs)==1:
            return qs[0].id

        qs = Country.objects.filter(code2__istartswith=name)
        if len(qs)==1:
            return qs[0].id

        qs = Country.objects.filter(code3__istartswith=name)
        if len(qs)==1:
            return qs[0].id

        qs = Country.objects.filter(alternate_names__icontains=name)
        if len(qs)==1:
            return qs[0].id
        if '(us)' in name:
            return Country.objects.get(name='United States').id
        return None

    def find_city(self, country_id, city_name):

        if country_id:
            qs = City.objects.filter(country__id=country_id)
        else:
            qs = City.objects.all()

        qs2 = qs.filter(name__icontains=city_name)
        if len(qs2)==1:
            return qs2[0].id

        m = re.match('(.*) \((.*)\)', city_name)
        if m:
            m = m.groups()
            city_name = m[0]
            region = m[1]

            qs2 = qs.filter(name=city_name)
            if len(qs2)==1:
                return qs2[0].id
            else:
                qs3 = qs2.filter(region__name=region)
                if len(qs3)==1:
                    return qs3[0].id

            

        print('FAIL: ', city_name)

    def process_charts(self, text):
        pattern = re.compile("(.*) \((.+?)\), (.+?), (.+?), (.+?)Edit")
        #text  = self.cleaned_data['text']
        charts = []

        for i, line in enumerate(text.split('\n')):
            m = re.match(pattern,line)
            if m:
                m = m.groups()
                d = {'name':m[0],
                'gender': m[1],
                'date':self.parse_date(m[2])['date'],
                'time':self.parse_date(m[2])['time'],
                }
                d['country'] = self.find_country(m[4])
                d['city'] = self.find_city(d['country'], m[3])
                charts.append(d)
        return charts

    def parse_date(self, s):
        dic = {'date':'', 'time':''}

        if 'unknown time' in s:
            s = s.replace('unknown time', '')
            return {'date':parse(s).date(), 'time':''}
        d = parse(s)
        if d:
            dic = {'date':d.date(), 'time':d.time()}
        return dic

    def done(self, form_list, **kwargs):
        #do_something_with_the_form_data(form_list)
        with transaction.atomic():
            for form in list(form_list)[1]:
                form.instance.owner = self.request.user
                form.save()

        return HttpResponseRedirect(reverse_lazy('chart:list'))
