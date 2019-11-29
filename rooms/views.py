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
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    baths = int(request.GET.get("baths", 0))
    beds = int(request.GET.get("beds", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))

    selected_country = request.GET.get("country", "JP")
    selected_room_type = request.GET.get("room_type", 0)
    selected_amenities = request.GET.getlist("amenities")
    selected_facilities = request.GET.getlist("facilities")

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    city = str.capitalize(city)

    form = {
        "city": city,
        "price": int(price),
        "guests": int(guests),
        "bedrooms": int(bedrooms),
        "baths": int(baths),
        "beds": int(beds),
        "instant": instant,
        "superhost": superhost,
        "selected_room_type": int(selected_room_type),
        "selected_country": selected_country,
        "selected_amenities": selected_amenities,
        "selected_facilities": selected_facilities,
    }

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    if selected_room_type != 0:
        filter_args["room_type__pk__exact"] = selected_room_type

    if price != 0:
        filter_args["price__lte"] = price

    if guests != 0:
        filter_args["guests__gte"] = guests

    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    if beds != 0:
        filter_args["beds__gte"] = beds

    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    if len(selected_amenities) > 0:
        for selected_amenity in selected_amenities:
            filter_args["amenities__pk"] = int(selected_amenity)

    if len(selected_facilities) > 0:
        for selected_facility in selected_facilities:
            filter_args["facilities_pk"] = int(selected_facility)

    filter_args["country"] = selected_country

    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request, "rooms/room_search.html", {**form, **choices, "rooms": rooms}
    )

