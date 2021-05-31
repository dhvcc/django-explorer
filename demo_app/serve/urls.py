from django.conf import settings
from django.urls import path

from django_explorer import PlainExplorerView

urlpatterns = [
    path("", PlainExplorerView.as_include(root=settings.BASE_DIR / "data_dir")),
]
