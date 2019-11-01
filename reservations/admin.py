from django.contrib import admin
from . import models


@admin.register(models.Reservation)
class Reservation(admin.ModelAdmin):

    """ Reservation Model Definition """

    list_display = ("room", "status", "check_in", "check_out", "guest", "in_progress")

