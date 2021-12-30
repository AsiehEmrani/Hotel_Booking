from rest_framework import serializers
from .models import Booking
from room.serializers import *
from model_utils.choices import Choices
from utils.commen import IdSerializer


class BookingSerializers(serializers.ModelSerializer):

    class Meta:
        model = Booking
        fields = ('room', 'email', 'checkin_date', 'checkout_date')


class ShowBookingSerializers(serializers.Serializer):
    hotel = HotelSerializers()
    room = RoomSerializers()
    id = serializers.CharField(max_length=255)
    checkin_date = serializers.DateField()
    checkout_date = serializers.DateField()


class ShowBillSerlializers(serializers.Serializer):
    id = serializers.CharField(max_length=255)
    booking = ShowBookingSerializers()
    created_at = serializers.DateTimeField()
    price = serializers.FloatField()


class SearchSerializers(serializers.Serializer):
    status_choices = Choices(
        'all',
    )
    city = serializers.CharField(max_length=255, required=False)
    # hotel_id = serializers.CharField(max_length=255, required=False)
    checkin_date = serializers.DateTimeField(required=True)
    checkout_date = serializers.DateTimeField(required=True)
    status = serializers.ChoiceField(choices=status_choices, required=False)


class ShowGuestBookingSerializers(serializers.Serializer):
    email = serializers.EmailField()