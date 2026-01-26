from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def loginView(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip().lower()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('adminDashboard')
            else:
                return redirect('teacherDashboard')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')

def teacherDashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return render(request, 'teacherDashboard.html', {'username': request.user.username})

def adminDashboard(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    return render(request, 'adminDashboard.html', {'username': request.user.username})
