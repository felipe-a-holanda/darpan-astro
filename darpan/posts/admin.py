from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Post


class PostAdmin(admin.ModelAdmin):
    def tag_list(self, obj):
        
        display_text = ", ".join([
            "<a href={}>{}</a>".format(
                    reverse('admin:{}_{}_change'.format('taggit', 'tag'),
                    args=(child.pk,)),
                child.name)
             for child in obj.tags.all()
        ])
        if display_text:
            return mark_safe(display_text)
        return "-"
    
    list_display = ('title', 'owner', 'tag_list')
    
admin.site.register(Post, PostAdmin)
