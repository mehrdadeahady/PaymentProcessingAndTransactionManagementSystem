# URL helpers.
from django.urls import path

# Views.
from .views import (

    RegisterAPIView,

    EmailTokenObtainAPIView
)


urlpatterns = [

    # Registration.
    path(

        "register/",

        RegisterAPIView.as_view(),

        name="register"
    ),

    # Email login.
    path(

        "login/",

        EmailTokenObtainAPIView.as_view(),

        name="login"
    ),
]