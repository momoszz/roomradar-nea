from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    roomName = models.CharField(max_length=20, unique=True)
    capacity = models.IntegerField()
    hasProjector = models.BooleanField(default=False)
    hasComputers = models.BooleanField(default=False)
    blockLocation = models.CharField(max_length=30)

    def __str__(self):
        return self.roomName

class Booking(models.Model):
    bookingID = models.AutoField(primary_key=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    bookingDate = models.DateField()
    periodNumber = models.IntegerField()
    subject = models.CharField(max_length=50)
    classSize = models.IntegerField()

    def __str__(self):
        return f'{self.room.roomName} - Period {self.periodNumber}'


