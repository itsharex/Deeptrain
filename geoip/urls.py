from django.urls import path
from .views import *

urlpatterns = [
    path("", request_map, name="index"),
    path("city/", country, name="country"),
    path("country/", city, name="city"),
    path("analysis/", analysis_request, name="analysis"),
]
