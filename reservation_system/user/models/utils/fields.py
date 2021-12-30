from .validators import validate_phone_number, validate_phone_format, validate_national_id
from django.db.models.fields import CharField


class PhoneNumberField(CharField):
    description = 'Phone number'
    max_length = 32

    default_validators = [
        validate_phone_format,
        validate_phone_number,
    ]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self.max_length
        super(PhoneNumberField, self).__init__(*args, **kwargs)


class NationalIDField(CharField):
    description = 'National ID'
    max_length = 10

    default_validators = [
        validate_national_id
    ]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = self.max_length
        super(NationalIDField, self).__init__(*args, **kwargs)
