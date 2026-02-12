from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Room, Booking
from datetime import date, timedelta

# Handles user login with username normalization and role-based routing
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip().lower()  # Prevents case/spacing issues
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # Uses Django's secure password hashing
        if user is not None:
            login(request, user)  # Creates session token
            if user.is_staff:
                return redirect('adminDashboard')  # Admins go to red dashboard
            else:
                return redirect('teacherDashboard')  # Teachers go to blue dashboard
        else:
            messages.error(request, 'Invalid username or password')  # Vague message prevents username enumeration
    return render(request, 'login.html')

# Teacher dashboard displaying room availability grid for current week
def teacherDashboard(request):
    if not request.user.is_authenticated:  # Blocks direct URL access
        return redirect('login')
    
    # Calculate current week's Monday and Friday
    today = date.today()
    weekday = today.weekday()  # Monday=0, Sunday=6
    weekStart = today - timedelta(days=weekday)  # Go back to Monday
    weekEnd = weekStart + timedelta(days=4)  # Friday is 4 days after Monday
    
    # Query all rooms and bookings for current week in single queries (avoids N+1 problem)
    allRooms = Room.objects.all()
    allBookings = Booking.objects.filter(
        bookingDate__gte=weekStart,
        bookingDate__lte=weekEnd
    ).select_related('room', 'teacher')  # Fetch related room and teacher data in same query
    
    # Build lookup dictionary: (roomID, periodNumber, weekday) -> booking object
    bookingLookup = {}
    for booking in allBookings:
        key = (booking.room.id, booking.periodNumber, booking.bookingDate.weekday())
        bookingLookup[key] = booking
    
    # Define periods and weekdays for template loops
    periods = list(range(1, 7))  # Periods 1-6
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
        'bookingLookup': bookingLookup,  # Passed to template for instant lookup
        'weekStart': weekStart,
        'weekEnd': weekEnd
    }
    return render(request, 'teacherDashboard.html', context)

# Admin dashboard view with authentication and privilege check
def adminDashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:  # Must be logged in AND admin
        return redirect('login')
    return render(request, 'adminDashboard.html', {'username': request.user.username})
