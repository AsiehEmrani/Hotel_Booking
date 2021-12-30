from rest_framework import serializers
from .models import Room, RoomType, Hotel


class RoomTypeSerializers(serializers.ModelSerializer):

    class Meta:
        model = RoomType
        fields = ('extra_bed', 'room_type')


class HotelSerializers(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('name', 'city', 'num_rooms', 'address', 'star_rating', 'phone_number', 'code')


class RoomSerializers(serializers.ModelSerializer):
    room_type = RoomTypeSerializers()
    hotel_code = HotelSerializers()

    class Meta:
        model = Room
        fields = ('id', 'hotel_code', 'room_type', 'price', 'occupancy')
