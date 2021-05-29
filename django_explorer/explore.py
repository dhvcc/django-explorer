from pathlib import Path
from typing import List, Optional, Union

from django.urls import include, path
from django.urls.resolvers import URLPattern

from django_explorer import themes
from django_explorer.settings import get_explorer_settings


def get_directory_view(root: Path, directory_name: Optional[str]):
    settings = get_explorer_settings()

    theme_module = getattr(themes, settings.theme)
    preview_function = getattr(theme_module, "get_file_preview")
    list_function = getattr(theme_module, "get_list")

    directory_name = directory_name or root.name

    def directory_view(request, relative: str = ""):
        current = root / relative

        if current.is_file():
            return preview_function(current)

        return list_function(request, root, current, settings.glob)

    return directory_view


def explore(
    root_path: Union[str, Path],
    *,
    reverse_name: str = "directory_view",
    directory_name: Optional[str] = None,
) -> List[URLPattern]:
    """
    A funtion to return url patterns for directory listing.

    :return: A list of 2 URLPattern objects
    """

    root = Path(root_path)

    if not root.is_dir():
        raise ValueError("root_path argument should be a directory")

    urlpatterns = [
        path(
            "",
            get_directory_view(root, directory_name),
            name=reverse_name + "_root",
        ),
        path(
            "<str:relative>",
            get_directory_view(root, directory_name),
            name=reverse_name,
        ),
    ]
    return include(urlpatterns)
