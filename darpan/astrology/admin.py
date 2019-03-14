from django.contrib import admin

from django_reverse_admin import ReverseModelAdmin


from .models import AstroChart


SIGNS = ["Aries",
                  "Taurus",
                  "Gemini",
                  "Cancer",
                  "Leo",
                  "Virgo",
                  "Libra",
                  "Scorpio",
                  "Sagittarius",
                  "Capricorn",
                  "Aquarius",
                  "Pisces"]



class field(object):
    def __init__(self, short_description, admin_order_field):
        self.short_description = short_description
        self.admin_order_field = admin_order_field
    
    def __call__(self, original_func):
        decorator_self = self
        def wrappee( *args, **kwargs):
            return original_func(*args,**kwargs)
        
        wrappee.short_description = self.short_description
        wrappee.admin_order_field = self.admin_order_field
        return wrappee


def dms(float_degrees):
    d = int(float_degrees)
    m = int((float_degrees - d)*60)
    s = int(((float_degrees - d)-m/60)*60*60)
    return d,m,s


def get_planet_sign(planet_name):
    def wrappee(self, obj):
        g = getattr(obj, planet_name)
        d = g - int(g/30)*30
        d,m,s = dms(d)
        return "%s %dº %d' %d\"" % (SIGNS[int(g/30)], d,m,s)
    wrappee.short_description = planet_name
    wrappee.admin_order_field = planet_name
    return wrappee    


class AstroChartAdmin(ReverseModelAdmin):
#class AstroChartAdmin(admin.ModelAdmin):

    inline_type = 'stacked'
    inline_reverse = ['chart']
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(AstroChartAdmin, self).get_inline_instances(request, obj)
    
    readonly_fields = ( 'sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto')

    @field('Name', 'chart__name')
    def get_name(self, obj):
        return obj.chart.name

    @field('Owner', 'chart__owner')
    def get_owner(self, obj):
        return obj.chart.owner

    @field('Birthday', 'chart__datetime_utc')
    def get_datetime(self, obj):
        return obj.chart.datetime_utc

    get_sun = get_planet_sign('sun')
    get_moon = get_planet_sign('moon')
    get_mercury = get_planet_sign('mercury')
    get_venus = get_planet_sign('venus')
    get_mars = get_planet_sign('mars')

    list_display = ('get_name', 'get_owner', 'get_datetime', 'get_sun', 'get_moon', 'get_mercury', 'get_venus', 'get_mars')

admin.site.register(AstroChart, AstroChartAdmin)

