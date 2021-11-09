from django.contrib import admin

from .models import Listing,ListingRecord, ListingSnapshot

# Inlines

class ListingRecordInline(admin.TabularInline):
    model = ListingRecord
    readonly_fields = ['created_at','price','num_favorers']

# Admins

class ListingAdmin(admin.ModelAdmin):
    inlines = [ListingRecordInline,]
    search_fields = ['shop__name', 'title', ]

class ListingSnapshotAdmin(admin.ModelAdmin):
    inlines = [ListingRecordInline,]
    search_fields = ['shop__name', 'title', ]
        
class ListingRecordAdmin(admin.ModelAdmin):
    search_fields = ['listing__title', 'price', 'quantity','num_favorers', ]

# Registers

admin.site.register(Listing,ListingAdmin)
admin.site.register(ListingSnapshot, ListingSnapshotAdmin)
admin.site.register(ListingRecord,ListingRecordAdmin)
