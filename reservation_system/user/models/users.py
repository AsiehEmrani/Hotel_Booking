from django.db import models
from django.contrib.auth.models import AbstractUser
from user.models.utils.fields import PhoneNumberField, NationalIDField


class User(AbstractUser):
    Gender = (
        ('M', 'male'),
        ('F', 'Female')
    )
    gender = models.CharField(max_length=255, choices=Gender, null=True)
    phone_number = PhoneNumberField()
    national_id = NationalIDField()
    email = models.EmailField(max_length=255, null=True)


class Customer(User):
    address = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=255, null=True)


class Guest(models.Model):
    name = models.CharField(max_length=255)
    phone_number = PhoneNumberField()
    email = models.EmailField(max_length=255, null=True)