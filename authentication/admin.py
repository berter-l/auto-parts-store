from django.contrib import admin

from authentication.adminforms import UserAdninForm
from authentication.models import CustomUser


class PersonAdmin(admin.ModelAdmin):
    form = UserAdninForm
    search_fields = ['username', 'email']
    list_filter = ['is_staff', 'is_superuser']
    list_display = ['username', 'email', 'is_staff', 'is_superuser']


admin.site.register(CustomUser, PersonAdmin)
