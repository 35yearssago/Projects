from django.core.exceptions import ValidationError


def validate_first_name(value):
    if not value[0].isalpha():
        raise ValidationError("Your name must start with a letter!")


def fruit_name_validator(value):
    if not value.isalpha():
        raise ValidationError("Fruit name should contain only letters!")
