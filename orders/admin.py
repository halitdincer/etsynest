from django.contrib import admin

from .models import Order

class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_id','first_name']

admin.site.register(Order,OrderAdmin)
