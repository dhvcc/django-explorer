from pathlib import Path
from typing import Optional, Union

from django.shortcuts import render
from django.urls import include, path


def get_directory_view(root_path):
    def directory_view(request, relative_path: Optional[str] = None):
        print(f"{root_path}/{relative_path}")
        return render(
            request,
            "django_explorer/plain.html",
            context={"path": f"{root_path}/{relative_path}"},
        )

    return directory_view


def explore(root_path: Union[str, Path], *, path_name: Optional[str] = None):
    urlpatterns = [
        path(
            "<str:relative_path>",
            get_directory_view(root_path),
            name=path_name or "directory_view",
        )
    ]
    return include(urlpatterns)
