from django.urls import path
from .views import BookingView, SearchView

urlpatterns = [
    path('', BookingView.as_view()),
    path('search/', SearchView.as_view())
]