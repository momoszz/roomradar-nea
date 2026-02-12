from django import template

register = template.Library()

# Custom filter to lookup booking by (roomID, period, weekday) tuple key
@register.filter(name='get_booking')
def getBooking(bookingDict, args):
    """Looks up booking in dictionary using comma-separated args as tuple key"""
    try:
        roomID, period, weekday = args.split(',')
        key = (int(roomID), int(period), int(weekday))
        return bookingDict.get(key, None)
    except (ValueError, AttributeError):
        return None  # Returns None if lookup fails (cell will show as available)
