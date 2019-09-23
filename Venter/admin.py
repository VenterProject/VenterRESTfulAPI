import datetime
from django.utils import timezone

from django.contrib import admin
from django.contrib.admin.filters import DateFieldListFilter
from django.utils.translation import gettext_lazy as _

from Venter.models import (Category, File, Organisation, UserCategory,
                           UserComplaint)


# class ICMCDateTimeFilter(DateFieldListFilter):
#     def __init__(self, *args, **kwargs):
#         super(ICMCDateTimeFilter, self).__init__(*args, **kwargs)

#         # now = timezone.now()
#         # if timezone.is_aware(now):
#         #     now = timezone.localtime(now)

#         today = datetime.datetime.now(tz=timezone.utc)

#         self.links += ((
#             (_('Past 2 weeks'), {
#                 self.lookup_kwarg_since: str(today),
#                 self.lookup_kwarg_until: str(today - datetime.timedelta(days=14)),
#             }),
#         ))

class OrganisationAdmin(admin.ModelAdmin):
    list_display = ('organisation_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)

class FileAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'ckpt_date')
    list_filter = ['organisation_name']

class UserComplaintAdmin(admin.ModelAdmin):
    list_display = ('organisation_name', 'user_complaint', 'creation_date')
    list_filter = ['organisation_name', 'creation_date']

class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('user_category', 'user_complaint')


admin.site.register(Organisation, OrganisationAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(UserComplaint, UserComplaintAdmin)
admin.site.register(UserCategory, UserCategoryAdmin)
