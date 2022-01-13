from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Driver, Client, Order


# Register your models here.

@admin.register(Driver)
class DriverAdmin(UserAdmin):
    list_display = ('id', 'car', 'car_number', 'last_name',)
    list_filter = ('car',)
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
        (_('Permissions'), {
            'fields': ('is_active',),
        }),
        (_('Important dates'), {'fields': ('date_joined',)}),
        (_('Car'), {'fields': ('car','car_number',)}),
    )

@admin.register(Client)
class ClientAdmin(UserAdmin):
    list_display = ('id', 'nationality',)
    list_filter = ('nationality',)
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email',)}),
        (_('Permissions'), {
            'fields': ('is_active',),
        }),
        (_('Important dates'), {'fields': ('date_joined',)}),
        (_('Millati'), {'fields': ('nationality',)}),

    )

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Order._meta.get_fields()]
    search_fields = ('driver_id', 'client_id',)
    list_filter = ('date',)
