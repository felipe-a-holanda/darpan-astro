from django.contrib import admin
from django_reverse_admin import ReverseModelAdmin
# Register your models here.


from .models import *
from charts.models import Chart

class ChartInline(admin.StackedInline):
    model = Chart
    #can_delete = False
    #verbose_name_plural = 'Chart'
    #fk_name = 'ravechart'
    #readonly_fields = ( 'birthday',)


class RaveChartAdmin(ReverseModelAdmin):

    #inlines = (ChartInline, )
    inline_type = 'stacked'
    inline_reverse = ['chart']

   

    def get_name(self, obj):
        return obj.chart.name
    get_name.admin_order_field  = 'name'  #Allows column order sorting
    get_name.short_description = 'Name'  #Renames column head


    def get_owner(self, obj):
        return obj.chart.owner
    get_owner.admin_order_field  = 'owner'  #Allows column order sorting
    get_owner.short_description = 'Owner'  #Renames column head

    def get_datetime(self, obj):
        return obj.chart.datetime_utc
    get_datetime.admin_order_field  = 'datetime_utc'  #Allows column order sorting
    get_datetime.short_description = 'Birthday'  #Renames column head


    list_display = ('get_name', 'get_owner', 'get_datetime')
    readonly_fields = ('gates', 'channels')



    
class GateAdmin(admin.ModelAdmin):
    pass

class ChannelAdmin(admin.ModelAdmin):
    
    def get_name(self, obj):
        
        return "(%d-%d) %s" % (obj.gate1.number, obj.gate2.number, obj.name)
    get_name.short_description = 'name'
    
    list_display = ('get_name', 'gate1', 'gate2', 'circuit', 'circuit_group')
    list_filter = ['circuit_group', 'circuit']
    
    #inlines = [GateInline]

admin.site.register(RaveChart, RaveChartAdmin)
admin.site.register(Gate, GateAdmin)
admin.site.register(Channel, ChannelAdmin)
