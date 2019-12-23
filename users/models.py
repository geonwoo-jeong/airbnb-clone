from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db import models


class User(AbstractUser):

    """ Custom User Model """

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE, "Female"),
        (GENDER_OTHER, "Other"),
    )

    LANGUAGE_ENGLISH = "en"
    LANGUAGE_KOREAN = "kr"
    LANGUAGE_JAPANESE = "jp"

    LANGUAGE_CHOICE = (
        (LANGUAGE_ENGLISH, "English"),
        (LANGUAGE_KOREAN, "Korean"),
        (LANGUAGE_JAPANESE, "Japanese"),
    )

    CURRENCY_USD = "usd"
    CURRENCY_KRW = "krw"
    CURRENCY_JPY = "jpy"

    CURRENCY_CHOICE = (
        (CURRENCY_USD, "USD"),
        (CURRENCY_KRW, "KRW"),
        (CURRENCY_JPY, "JPY"),
    )

    avatar = models.ImageField(upload_to="avatars", blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=10, blank=True)
    bio = models.TextField(blank=True)
    birthdate = models.DateField(blank=True, null=True)
    language = models.CharField(
        choices=LANGUAGE_CHOICE, max_length=2, blank=True, default=LANGUAGE_JAPANESE
    )
    currency = models.CharField(
        choices=CURRENCY_CHOICE, max_length=3, blank=True, default=CURRENCY_JPY
    )
    superhost = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    email_secret = models.CharField(max_length=128, default="", blank=True)

    def verify_email(self):
        pass

    def get_absolute_url(self):
        return reverse("users:id", kwargs={self.id})

