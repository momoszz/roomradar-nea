from django import template
from datetime import timedelta

register = template.Library()

# custom tag to look up bookings
@register.simple_tag(name='get_booking')
def getBooking(bookingDict, roomId, period, weekday):
    try:
        key = (int(roomId), int(period), int(weekday))
        return bookingDict.get(key, None)
    except (ValueError, AttributeError):
        return None

# calculates date by adding days to a start date
@register.filter(name='add_days')
def addDays(startDate, days):
    return startDate + timedelta(days=days)
