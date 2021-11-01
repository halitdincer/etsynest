from django.contrib import admin

from .models import Shop
from listings.models import Listing

# Inlines
class ListingInline(admin.TabularInline):
    model = Listing
    extra = 0
    fields = ['title', ]
    readonly_fields = ['title', ]

    def has_delete_permission(self, request, obj=None):
        return False

# Admins


class ShopAdmin(admin.ModelAdmin):
    inlines = [ListingInline, ]




# Registers
admin.site.register(Shop,ShopAdmin)

