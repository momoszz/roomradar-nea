from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

# handles user login with username normalization and role-based routing
def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip().lower()  # prevents case/spacing issues
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)  # uses Django's secure password hashing
        if user is not None:
            login(request, user)  # creates session token
            if user.is_staff:
                return redirect('adminDashboard')
            else:
                return redirect('teacherDashboard')
        else:
            messages.error(request, 'Invalid username or password')  # Vague message prevents username enumeration
    return render(request, 'login.html')

# Teacher dashboard view with authentication guard
def teacherDashboard(request):
    if not request.user.is_authenticated:  # blocks direct URL access
        return redirect('login')
    return render(request, 'teacherDashboard.html', {'username': request.user.username})

# Admin dashboard view with authentication and privileges check
def adminDashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:  # must be logged in AND an admin
        return redirect('login')
    return render(request, 'adminDashboard.html', {'username': request.user.username})



-