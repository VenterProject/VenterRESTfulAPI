from django.contrib import admin
from Venter.models import Category, Organisation, File
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_filter=['organisation']

class FileAdmin(admin.ModelAdmin):
    model = File
    list_filter=['organisation']
    list_display=['organisation', 'ckpt_date']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Organisation)
admin.site.register(File, FileAdmin)