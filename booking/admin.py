from django.contrib import admin
from .models import Booking


# Register your models here.
class bookingAdmin(admin.ModelAdmin):
    # Fields to show in the admin form
    list_display = ('user', 'location', 'booking_date')
admin.site.register(Booking, bookingAdmin)