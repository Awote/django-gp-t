# myapp/urls.py
from django.urls import path
from .views import UploadCsvView

urlpatterns = [
    path('upload-csv/', UploadCsvView.as_view(), name='upload-csv'),
]
