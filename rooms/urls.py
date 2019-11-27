from django.urls import path
from . import views

app_name = "rooms"

# DetailView is automatically find <pk>
urlpatterns = [path("<int:pk>", views.RoomDetail.as_view(), name="detail")]

