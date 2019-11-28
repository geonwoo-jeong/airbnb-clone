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
    city = str.capitalize(city)
    room_types = models.RoomType.objects.all()
    return render(
        request,
        "rooms/room_search.html",
        {"city": city, "countries": countries, "room_types": room_types},
    )
