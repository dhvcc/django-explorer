from django.conf import settings
from django.urls import path

from django_explorer.views import BaseExplorerView

urlpatterns = [
    path("", BaseExplorerView(root=settings.BASE_DIR / "data_dir")),
]
