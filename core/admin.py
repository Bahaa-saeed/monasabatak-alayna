from django.contrib import admin
from .models import Venue, Vendor, Service, EventRequest, Offer, Booking

admin.site.site_header = "مناسبتك علينا | إدارة المنصة"
admin.site.site_title = "إدارة مناسبتك علينا"
admin.site.index_title = "إدارة الحجوزات والخدمات"

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ("name", "venue_type", "city", "capacity", "price_from", "is_active")
    list_filter = ("venue_type", "city", "is_active")
    search_fields = ("name", "city", "area")
    list_editable = ("is_active",)

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "city", "phone", "is_active")
    list_filter = ("category", "city", "is_active")
    search_fields = ("name", "category", "city")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "vendor", "starting_price", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name",)

@admin.register(EventRequest)
class EventRequestAdmin(admin.ModelAdmin):
    list_display = ("reference", "customer_name", "event_type", "city", "event_date", "status", "created_at")
    list_filter = ("status", "event_type", "city", "event_date")
    search_fields = ("reference", "customer_name", "phone")
    readonly_fields = ("reference", "created_at")
    filter_horizontal = ("requested_services",)
    date_hierarchy = "created_at"

class OfferInline(admin.TabularInline):
    model = Offer
    extra = 0

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "request", "venue", "total_price", "is_selected", "created_at")
    list_filter = ("is_selected",)
    search_fields = ("title", "request__reference", "request__customer_name")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("offer", "status", "deposit_amount", "paid_amount", "coordination_fee", "commission_amount")
    list_filter = ("status",)
    search_fields = ("offer__request__reference", "offer__request__customer_name")
