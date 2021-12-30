from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    num_rooms = models.IntegerField()
    address = models.CharField(max_length=255)
    star_rating = models.IntegerField()
    phone_number = models.IntegerField()
    code = models.IntegerField()


class RoomType(models.Model):

    class Type(models.TextChoices):
        Double = ('D', 'double')
        Twin = ('T', 'twin')
        Single = ('S', 'single')
        Triple = ('Tri', 'triple')
        Quad = ('q', 'quad')

    extra_bed = models.BooleanField(default=False)
    room_type = models.CharField(max_length=20, choices=Type.choices)


class Room(models.Model):
    hotel_code = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.OneToOneField(RoomType, on_delete=models.SET_NULL, null=True)
    price = models.FloatField()
    occupancy = models.BooleanField(default=False)



