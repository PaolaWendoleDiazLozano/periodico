# paginas/urls.py
from django.urls import path

from .views import VistaInicio

urlpatterns = [
    path("", VistaInicio.as_view(), name="inicio"),
]
