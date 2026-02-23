from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Room, Booking
from datetime import date, timedelta, datetime

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

# teacher dashboard showing room availability grid for selected week
def teacherDashboard(request):
    if not request.user.is_authenticated:  # blocks direct url access
        return redirect('login')

    # get date offset from url, default to 0 for current week
    weekOffset = int(request.GET.get('offset', 0))

    # get selected room id for filtering
    roomId = request.GET.get('room')
    currentRoomId = int(roomId) if roomId else None
    
    # work out what week we're in - get monday and friday dates
    today = date.today() + timedelta(weeks=weekOffset)
    weekday = today.weekday()  # monday=0, sunday=6
    weekStart = today - timedelta(days=weekday)  # go back to this week's monday
    weekEnd = weekStart + timedelta(days=4)  # friday is 4 days after monday
    
    # get all rooms for dropdown
    allRooms = Room.objects.all()

    # filter rooms for display if a specific one is selected
    if currentRoomId:
        displayRooms = allRooms.filter(id=currentRoomId)
    else:
        displayRooms = allRooms

    # get bookings for the week
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

    # get upcoming bookings for the sidebar
    # filter by current user and dates from today onwards
    upcomingBookings = Booking.objects.filter(
        teacher=request.user,
        bookingDate__gte=date.today()
    ).order_by('bookingDate', 'periodNumber')

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
        'rooms': displayRooms,
        'allRooms': allRooms,
        'currentRoomId': currentRoomId,
        'periods': periods,
        'weekdays': weekdays,
        'bookingLookup': bookingLookup,
        'weekStart': weekStart,
        'weekEnd': weekEnd,
        'weekOffset': weekOffset,
        'prevOffset': weekOffset - 1,
        'nextOffset': weekOffset + 1,
        'upcomingBookings': upcomingBookings
    }
    return render(request, 'teacherDashboard.html', context)

# handles booking creation with validation and error checking
def bookRoom(request, roomId, period, dateStr):
    if not request.user.is_authenticated:
        return redirect('login')

    # get the room and parse the date from url string
    room = get_object_or_404(Room, pk=roomId)
    bookingDate = datetime.strptime(dateStr, '%Y-%m-%d').date()

    if request.method == 'POST':
        className = request.POST.get('className')
        classSize = int(request.POST.get('classSize'))

        # check if class size fits in the room
        if classSize > room.capacity:
            messages.error(request, f'Class size ({classSize}) exceeds room capacity ({room.capacity})')
        else:
            # check if slot is still available just in case
            isTaken = Booking.objects.filter(
                room=room,
                bookingDate=bookingDate,
                periodNumber=period
            ).exists()

            if isTaken:
                messages.error(request, 'This slot has already been booked')
            else:
                # create the booking record
                Booking.objects.create(
                    room=room,
                    teacher=request.user,
                    bookingDate=bookingDate,
                    periodNumber=period,
                    className=className,
                    classSize=classSize
                )
                messages.success(request, 'Room booked successfully')
                return redirect('teacherDashboard')

    context = {
        'room': room,
        'period': period,
        'bookingDate': bookingDate,
        'username': request.user.username
    }
    return render(request, 'bookRoom.html', context)

# handles booking edits and deletions
def editBooking(request, bookingId):
    if not request.user.is_authenticated:
        return redirect('login')

    # get booking or 404, verify ownership
    booking = get_object_or_404(Booking, pk=bookingId)

    # prevent editing other people's bookings
    if booking.teacher != request.user:
        messages.error(request, 'You can only edit your own bookings')
        return redirect('teacherDashboard')

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'delete':
            booking.delete()
            messages.success(request, 'Booking cancelled successfully')
            return redirect('teacherDashboard')

        elif action == 'update':
            className = request.POST.get('className')
            classSize = int(request.POST.get('classSize'))

            # check capacity again
            if classSize > booking.room.capacity:
                messages.error(request, f'Class size ({classSize}) exceeds room capacity ({booking.room.capacity})')
            else:
                booking.className = className
                booking.classSize = classSize
                booking.save()
                messages.success(request, 'Booking updated successfully')
                return redirect('teacherDashboard')

    context = {
        'booking': booking,
        'room': booking.room,
        'bookingDate': booking.bookingDate,
        'period': booking.periodNumber
    }
    return render(request, 'editBooking.html', context)

# admin dashboard view with authentication and privilege check
def adminDashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:  # must be logged in AND admin
        return redirect('login')
    return render(request, 'adminDashboard.html', {'username': request.user.username})
