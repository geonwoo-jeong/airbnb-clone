from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class Reservation(admin.ModelAdmin):

    """ Reservation Model Definition """

    pass
