from django.contrib import admin

from .models import NumerologyChart



class NumerologyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'full_name', 'birthday', 'destiny_number', 'life_path_number')
    
    readonly_fields = ('life_path_number', 'destiny_number', 'alternative_destiny_number')

admin.site.register(NumerologyChart, NumerologyAdmin)
