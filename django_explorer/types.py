import functools
from pathlib import Path
from typing import Literal

from django.http import HttpRequest
from django.template.context import RequestContext
from pydantic import BaseModel


class ExplorerSettings(BaseModel):
    DEFAULT_GLOB: str = "*"

    class Config:
        use_enum_values = True


class ExplorerFile(BaseModel):
    path: Path
    type: Literal["file", "directory"]
    href: str
    download_href: str

    @classmethod
    def from_path(cls, path: str, request: HttpRequest) -> "ExplorerFile":
        file_path = Path(path)
        file_type = "file" if file_path.is_file() else "directory"

        paths = [request.path.lstrip("/"), file_path.parts[-1]]
        base_explorer_path = "/".join(paths)
        if file_type == "file":
            href_link = f"{base_explorer_path}?preview"
        else:
            href_link = f"{base_explorer_path}?list"

        return cls(
            path=path,
            type=file_type,
            href="href={}".format(href_link),
            download_href=f"href={base_explorer_path}?download={path}",
        )


class ExplorerContext(BaseModel):
    request: HttpRequest
    root: Path
    current: Path

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def validate(function):
        @functools.wraps(function)
        def wrapper(context: RequestContext, *args, **kwargs):
            return function(ExplorerContext(**context.flatten()), *args, **kwargs)

        return wrapper
