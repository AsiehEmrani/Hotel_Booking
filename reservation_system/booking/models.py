from django.db import models
from room.models import Room
from room.models import Hotel
from user.models.users import User
import datetime
from datetime import timedelta


class Booking(models.Model):

    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    email = models.EmailField(null=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.hotel.name
    #
    # def charge(self):
    #     if self.check_out:
    #         if self.checkin_date==self.checkout_date:
    #             return self.room.rate
    #         else:
    #             time_delta = self.checkout_date - self.checkin_date
    #             total_time = time_delta.days
    #             total_cost =total_time*self.room.rate
    #             # return total_cost
    #             return total_cost
    #     else:
    #         return 'calculated when checked out'


class Bill(models.Model):
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)