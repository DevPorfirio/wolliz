from django.contrib import admin
from .models import Property, PropertyImage


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    inlines      = [PropertyImageInline]
    list_display = ["title", "property_type", "listing_type", "city", "price", "is_active"]
    list_filter  = ["property_type", "listing_type", "is_active", "state"]
    search_fields = ["title", "city", "address_line"]
