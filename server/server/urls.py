from django.urls import path
from .views import sign_in, voter

urlpatterns = [
    path('sign-in', sign_in),
    path('vote', voter),
]
