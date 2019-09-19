from django.contrib import admin
from Venter.models import Category, Organisation, File

# Register your models here.

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('organisation_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)

class FileAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'ckpt_date')
    list_filter = ['organisation_name']


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(File, FileAdmin)
