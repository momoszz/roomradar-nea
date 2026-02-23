from django import template
from datetime import timedelta

register = template.Library()

# custom filter to look up bookings using room id, period and day as a key
@register.filter(name='get_booking')
def getBooking(bookingDict, args):
    # takes comma separated values and turns them into a tuple for dictionary lookup
    # returns the booking if it exists, otherwise returns none so the cell shows available
    try:
        roomId, period, weekday = args.split(',')
        key = (int(roomId), int(period), int(weekday))
        return bookingDict.get(key, None)
    except (ValueError, AttributeError):
        return None

# calculates date by adding days to a start date
@register.filter(name='add_days')
def addDays(startDate, days):
    return startDate + timedelta(days=days)
