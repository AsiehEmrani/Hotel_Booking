from django.urls import path
from .views import RoomView, HotelView

urlpatterns = [
    path('', RoomView.as_view()),
    path('hotel/', HotelView.as_view())
]