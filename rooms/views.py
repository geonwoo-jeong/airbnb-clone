from django.views.generic import ListView, DetailView
from django.shortcuts import render
from django_countries import countries
from . import models


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"


# Class Based Detail View


class RoomDetail(DetailView):

    """ Room Detail Definition """

    model = models.Room
    # default pk_url_kwarg is pk
    # pk_url_kwarg = 'pk'


# Functional Based Detail View

# def room_detail(request, pk):
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/room_detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         raise Http404()


def search(request):
    city = request.GET.get("city", "Anywhere")
    country = request.GET.get("country", "JP")
    room_type = request.GET.get("room_type", 0)
    city = str.capitalize(city)
    room_types = models.RoomType.objects.all()

    form = {
        "city": city,
        "selected_room_type": int(room_type),
        "selected_country": country,
    }

    choices = {"countries": countries, "room_types": room_types}

    return render(request, "rooms/room_search.html", {**form, **choices})

