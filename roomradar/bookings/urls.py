from django.urls import path
from . import views

# url routing for bookings app
urlpatterns = [
    path('', views.loginView, name='login'),  # root url shows login page
    path('dashboard/teacher/', views.teacherDashboard, name='teacherDashboard'),
    path('dashboard/admin/', views.adminDashboard, name='adminDashboard'),
]
