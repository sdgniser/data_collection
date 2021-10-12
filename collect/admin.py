from django.contrib import admin
from django.utils.html import mark_safe

from .models import Applicant

@admin.register(Applicant)
class ApplicantAdmin(admin.ModelAdmin):
    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.photo.url}" alt="{str(obj.app_no)} ({str(obj.name)})" style="width: 150px; height: 200px">')

    def get_sign(self, obj):
        return mark_safe(f'<img src="{obj.sign.url}" alt="{str(obj.app_no)} ({str(obj.name)})" style="width: 200px; height: 100px">')

    get_photo.short_description = 'Photograph'
    get_sign.short_description = 'Signature'

    list_display = ('app_no', 'name', 'blood_group', 'get_photo', 'get_sign')
    list_filter = ('blood_group',)
    fieldsets = (
        ('Applicant Supplied Data', {
            'fields': ('app_no', 'name', 'blood_group', ('get_photo', 'get_sign',))
        }),
    )

    readonly_fields = ('blood_group', 'get_photo', 'get_sign')
    list_per_page = 20
