from django.urls import path
from . import views

urlpatterns = [
    path('', views.loginView, name='login'),
    path('dashboard/teacher/', views.teacherDashboard, name='teacherDashboard'),
    path('dashboard/admin/', views.adminDashboard, name='adminDashboard'),
]
