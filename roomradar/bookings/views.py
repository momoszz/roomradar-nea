from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Room, Booking
from datetime import date, timedelta

# handles user login with username normalization and role-based routing
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip().lower()  # prevents case/spacing issues
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # uses django's secure password hashing
        if user is not None:
            login(request, user)  # creates session token
            if user.is_staff:
                return redirect('adminDashboard')  # admins go to red dashboard
            else:
                return redirect('teacherDashboard')  # teachers go to blue dashboard
        else:
            messages.error(request, 'Invalid username or password')  # vague message prevents username enumeration
    return render(request, 'login.html')

# teacher dashboard showing room availability grid for current week
def teacherDashboard(request):
    if not request.user.is_authenticated:  # blocks direct url access
        return redirect('login')
    
    # work out what week we're in - get monday and friday dates
    today = date.today()
    weekday = today.weekday()  # monday=0, sunday=6
    weekStart = today - timedelta(days=weekday)  # go back to this week's monday
    weekEnd = weekStart + timedelta(days=4)  # friday is 4 days after monday
    
    # get all rooms and bookings in one go to avoid loads of database queries
    allRooms = Room.objects.all()
    allBookings = Booking.objects.filter(
        bookingDate__gte=weekStart,
        bookingDate__lte=weekEnd
    ).select_related('room', 'teacher')  # grabs related data in same query for speed
    
    # build a dictionary so we can look up bookings quickly in the template
    # key is (room id, period number, day of week), value is the booking object
    bookingLookup = {}
    for booking in allBookings:
        key = (booking.room.id, booking.periodNumber, booking.bookingDate.weekday())
        bookingLookup[key] = booking
    
    # periods 1-6 for the school day
    periods = list(range(1, 7))
    # weekdays with their numbers so template can do lookups
    weekdays = [
        {'name': 'Monday', 'number': 0},
        {'name': 'Tuesday', 'number': 1},
        {'name': 'Wednesday', 'number': 2},
        {'name': 'Thursday', 'number': 3},
        {'name': 'Friday', 'number': 4}
    ]
    
    context = {
        'username': request.user.username,
        'rooms': allRooms,
        'periods': periods,
        'weekdays': weekdays,
        'bookingLookup': bookingLookup,
        'weekStart': weekStart,
        'weekEnd': weekEnd
    }
    return render(request, 'teacherDashboard.html', context)

# admin dashboard view with authentication and privilege check
def adminDashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:  # must be logged in AND admin
        return redirect('login')
    return render(request, 'adminDashboard.html', {'username': request.user.username})
