from django.db import models
from django.core.validators import MinLengthValidator
from .validators import validate_first_name, fruit_name_validator


class Profile(models.Model):
    first_name = models.CharField(
        max_length=25,
        blank=False,
        null=False,
        validators=[MinLengthValidator(2), validate_first_name]
    )
    last_name = models.CharField(
        max_length=35,
        blank=False,
        null=False,
        validators=[MinLengthValidator(1), validate_first_name]
    )
    email = models.EmailField(
        max_length=40,
        blank=False,
        null=False
    )
    password = models.CharField(
        max_length=20,
        blank=False,
        null=False,
        validators=[MinLengthValidator(8)]
    )
    image_url = models.URLField(
        blank=True,
        null=True
    )
    age = models.IntegerField(
        blank=True,
        null=True,
        default=18
    )

    def __str__(self):
        return self.first_name


class Fruit(models.Model):
    name = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        validators=[MinLengthValidator(2), fruit_name_validator]
    )
    image_url = models.URLField(
        blank=False,
        null=False
    )
    description = models.TextField(
        blank=False,
        null=False
    )
    nutrition = models.TextField(
        blank=True,
        null=True
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)