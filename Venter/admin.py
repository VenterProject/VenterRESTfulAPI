from django.contrib import admin
from Venter.models import Category

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)   



admin.site.register(Category, CategoryAdmin)    
