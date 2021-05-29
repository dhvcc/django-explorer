from django.conf import settings
from django.urls import path

from django_explorer import explore

urlpatterns = [
    path("", explore(settings.BASE_DIR / "data_dir")),
]
