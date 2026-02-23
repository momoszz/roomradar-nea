from django.contrib import admin
from .models import Room, Booking

# register models so they appear in django admin panel for testing
admin.site.register(Room)
admin.site.register(Booking)
