from django.conf import settings
from django.urls import path

from django_explorer import explore

urlpatterns = [
    path("", explore(settings.BASE_DIR / "data_folder")),
    path("", explore(settings.BASE_DIR / "data_folder", reverse_name="data_folder_listing")),
]
