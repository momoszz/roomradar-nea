from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def loginView(request):
    if request.method == "POST":
        username = request.POST['username'].strip.lower()
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username OR password is incorrect')
    return render(request, 'login.html')

def dashboardView(request):
    return render(request,'teacherDashboard.html')
