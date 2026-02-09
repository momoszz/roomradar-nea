from django.contrib import admin
from .models import Room, Booking

# Register models so they appear in Django admin panel for testing
admin.site.register(Room)
admin.site.register(Booking)
