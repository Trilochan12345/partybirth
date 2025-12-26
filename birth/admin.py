from django.contrib import admin
from .models import Addon, TimeSlot, EventBooking, BookingAddon
from django.utils.html import mark_safe
@admin.register(Addon)
class AddonAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'image_preview')
    search_fields = ('name',)
    list_filter = ('price',)

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="60" height="60" style="object-fit:cover; border-radius:5px;" />')
        return "No Image"
    image_preview.short_description = 'Preview'

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('start_time', 'end_time')
    ordering = ('start_time',)

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('fname', 'email', 'phone', 'event_date', 'timing')

@admin.register(BookingAddon)
class BookingAddonAdmin(admin.ModelAdmin):
    list_display = ('booking', 'addon', 'quantity')
