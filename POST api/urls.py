/Application/urls.py

from django.urls import path
from .views import upload_csv

urlpatterns = [
    path('upload_csv/', upload_csv, name='upload_csv'),
]
