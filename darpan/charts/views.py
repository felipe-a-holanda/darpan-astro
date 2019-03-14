from django.shortcuts import render
from django.views import generic
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.db import transaction
from django.http import HttpResponseRedirect
# Create your views here.

from dateutil.parser import parse

from formtools.wizard.views import SessionWizardView as WizardView

from .models import Chart
from .forms import ChartForm, ImportChartForm, ChartFormSet
from .forms import *

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



class ChartListView(FormListView):
    model = Chart
    form_class = ChartForm

class ChartDetailView(generic.DetailView):
    model = Chart

class ChartCreateView(generic.CreateView):
    model = Chart
    fields = ['name', 'date', 'time', 'timezone', 'city', 'country']

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class ChartImportView(generic.edit.FormView):
     form_class = ImportChartForm
     template_name = 'charts/import.html'
     success_url = reverse_lazy('charts:import2')


     def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        charts = form.process_charts()
        return super().form_valid(form)


class MultipleChartCreate(generic.CreateView):
    model = Chart
    fields = ['name', 'date', 'time', 'city']
    template_name = 'charts/import_multiple_form.html'
    success_url = reverse_lazy('charts:list')

    def get_context_data(self, **kwargs):
        data = super(MultipleChartCreate, self).get_context_data(**kwargs)
        print(self.request.GET)
        if self.request.POST:
            data['charts'] = ChartFormSet(self.request.POST)
        else:
            data['charts'] = ChartFormSet(initial=[{'name':"Xuxu"}, {'name':'Beleza'}])
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        charts = context['charts']

        for form in charts:
            form.instance.owner = self.request.user

        with transaction.atomic():
            self.object = form.save()

            if charts.is_valid():
                charts.instance = self.object
                charts.save()
        return super(MultipleChartCreate, self).form_valid(form)



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


    def process_charts(self, text):
        pattern = re.compile("(.*) \((.+?)\), (.+?), (.+?), (.+?)Edit")
        #text  = self.cleaned_data['text']
        charts = []

        for i, line in enumerate(text.split('\n')):
            m = re.match(pattern,line).groups()
            d = {'name':m[0],
            'gender': m[1],
            'date':self.parse_date(m[2])['date'],
            'time':self.parse_date(m[2])['time'],
            'city':m[3],
            'country':m[4],
            }
            charts.append(d)
        return charts

    def parse_date(self, s):
        dic = {'date':'', 'time':''}

        if 'unknown time' in s:
            s = s.replace('unknown time', '')
            return {'date':parse(s).date(), 'time':''}
        d = parse(s)
        dic = {'date':d.date(), 'time':d.time()}
        return dic

    def done(self, form_list, **kwargs):
        #do_something_with_the_form_data(form_list)
        with transaction.atomic():
            for form in list(form_list)[1]:
                form.instance.owner = self.request.user
                form.save()

        return HttpResponseRedirect(reverse_lazy('chart:list'))
