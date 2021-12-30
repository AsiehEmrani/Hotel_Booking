from django.urls import path
from .views import UserView, UserRegistrationView


urlpatterns = [
    path('users/', UserView.as_view()),
    path('registration/', UserRegistrationView.as_view()),
    # path('register_guest/', GuestView.as_view() )
]