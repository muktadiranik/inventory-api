import os
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


alphanumeric = RegexValidator(r'^[a-zA-Z-,-.-_ ]+$',
                              'Only alphanumeric characters are allowed.'
                              )

phone_regex = RegexValidator(r'^[0-9-+ ]+$',
                             "Phone number must be entered in the format: '+9999-99999'. Up to 15 digits allowed."
                             )

email_regex = RegexValidator(regex=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                             message="Email must be entered in the format: 'yourmail@gamil.com' "
                             )

zip_regex = RegexValidator(regex=r'^\d{4,6}$',
                           message="Zip code must be entered in the format: 999999. Up to 6 digits allowed"
                           )


def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf', '.docx', '.doc', 'docm']
    if not ext.lower() in valid_extensions:
        raise ValidationError(
            'Unsupported file. Only PDF and DOC files are allowed.')


def quantity_validator(value):
    try:
        value = int(value)
        if value < 0:
            raise ValidationError("Quantity must be greater than 0")
    except ValueError:
        pass


def unit_price_validator(value):
    try:
        value = float(value)
        if value < 0:
            raise ValidationError("Unit price must be greater than 0")
    except ValueError:
        pass


def paid_amount_validator(value):
    try:
        value = float(value)
        if value < 0:
            raise ValidationError("Paid amount must be greater than 0")
    except ValueError:
        pass
