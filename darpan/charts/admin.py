from django.contrib import admin

# Register your models here.
from .models import Chart


class ChartAdmin(admin.ModelAdmin):
    list_display = ('name', 'datetime_utc', 'owner')
    readonly_fields = ('datetime_utc',)

admin.site.register(Chart, ChartAdmin)

