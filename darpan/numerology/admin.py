from django.contrib import admin

from .models import NumerologyChart



class NumerologyAdmin(admin.ModelAdmin):
    
    def get_queryset(self, request):
        return super(NumerologyAdmin, self).get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    
    list_display = ('full_name','owner',  'birthday', 'destiny_number', 'life_path_number', 'tag_list', )
    
    readonly_fields = ('life_path_number', 'destiny_number', 'alternative_destiny_number', 'tags')
    
    list_filter = ('destiny_number', 'life_path_number')

admin.site.register(NumerologyChart, NumerologyAdmin)
