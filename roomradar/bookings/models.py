from django.db import models
from django.contrib.auth.models import User

# Stores room information including equipment and location
class Room(models.Model):
    roomName = models.CharField(max_length=20, unique=True)  # unique prevents duplicate room codes
    capacity = models.IntegerField()
    hasProjector = models.BooleanField(default=False)
    hasComputers = models.BooleanField(default=False)
    blockLocation = models.CharField(max_length=30)  # which building the room is in

    def __str__(self):
        return self.roomName  # Shows room name in admin panel instead of 'Room object'

# Stores individual booking records linking teachers to rooms and periods
class Booking(models.Model):
    bookingID = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # deletes all bookings if room deleted
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)  # links booking to teacher account
    bookingDate = models.DateField()
    periodNumber = models.IntegerField()  # 1-6 for school periods
    subject = models.CharField(max_length=50)
    classSize = models.IntegerField()  # used to check room capacity

    def __str__(self):
        return f'{self.room.roomName} - Period {self.periodNumber}'  # readable format for admin

