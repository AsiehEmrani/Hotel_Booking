from django.core.exceptions import ValidationError
import re
import phonenumbers


def validate_national_id(value):
    national_id_digits = re.match(r"^\d{10}$",value)
    if national_id_digits is not None:
        check = int(value[9])
        remain = sum([int(value[x]) * (10 - x) for x in range(9)]) % 11
        if not ((2 > remain == check) or (remain >= 2 and check + remain == 11)):
            raise ValidationError(_("Invalid National ID."), code=400)
    else:
        raise ValidationError(_("Invalid National ID."), code=400)


def validate_phone_format(value):
    if not re.match('^[+][0-9]+$', value):
        raise ValidationError(
            'Enter phone number in "+xx..." or "+[country_code][national_code]" format where x is a number'
        )


def validate_phone_number(value):
    try:
        parsed_number = phonenumbers.parse(number=value)
    except phonenumbers.phonenumberutil.NumberParseException as e:
        raise ValidationError(
            'Phone number is not valid'
        )

    if not phonenumbers.is_valid_number(parsed_number):
        raise ValidationError(
            'Phone number is not correct'
        )