from rest_framework import serializers
from user.models.users import User, Guest
from user.models.utils.fields import PhoneNumberField
from model_utils.choices import Choices


class UserSerializers(serializers.ModelSerializer):
    phone_number = PhoneNumberField
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'is_superuser', 'is_staff', 'phone_number', 'email')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User(
                email=validated_data['email'],
                username=validated_data['username'],
                phone_number=validated_data['phone_number'],
                is_staff=validated_data['is_staff'],
                is_superuser=validated_data['is_superuser']
            )
            user.set_password(validated_data['password'])
            user.save()

            return user


class StatusShowUserInfoSerializers(serializers.Serializer):
    status = Choices(
        'all',
    )
    id = serializers.CharField(max_length=255, required=False)
    # username = serializers.CharField(max_length=255)
    # email = serializers.EmailField()
    # phone_number = serializers.CharField(max_length=255)
    status = serializers.ChoiceField(choices=status, required=False)
    # is_superuser = serializers.BooleanField()
    # is_staff = serializers.BooleanField()


class UserRegistrationSerializers(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            phone_number=validated_data['phone_number']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

class GuestSerializers(serializers.ModelSerializer):

        class Meta:
                model = Guest
                fields = ('id', 'phone_number', 'name', 'email')
