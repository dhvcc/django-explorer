import functools
from pathlib import Path
from typing import Literal

from django.http import HttpRequest
from django.template.context import RequestContext
from pydantic import BaseModel

from django_explorer.utils import format_byte_size


class ExplorerFile(BaseModel):
    path: Path
    type: Literal["file", "directory"]
    href: str
    download_href: str

    @staticmethod
    def calculate_href(path: Path, request: HttpRequest) -> str:
        """Calculate href from request and file path."""

        base_url = request.path
        if base_url.lstrip("/"):
            base_url += "/"

        href = f"href={base_url}{path.name}"
        return href

    @classmethod
    def from_path(cls, path: str, request: HttpRequest) -> "ExplorerFile":
        file_path = Path(path)
        file_type = "file" if file_path.is_file() else "directory"

        href = cls.calculate_href(file_path, request)

        return cls(
            path=path,
            type=file_type,
            href=href,
            download_href=f"{href}?download",
        )

    @property
    def readable_size(self):
        return format_byte_size(self.path.stat().st_size)

    def __lt__(self, other: "ExplorerFile") -> bool:
        return self.path.name < other.path.name


class ExplorerContext(BaseModel):
    root: Path
    relative: Path
    current: Path

    @classmethod
    def from_relative(cls, root: str, relative: str) -> "ExplorerContext":
        root = Path(root)
        relative = Path(relative)
        return cls(
            root=root,
            relative=relative,
            current=root / relative,
        )

    @staticmethod
    def validate_tag(function):
        @functools.wraps(function)
        def wrapper(context: RequestContext, *args, **kwargs):
            return function(ExplorerContext(**context.flatten()), *args, **kwargs)

        return wrapper

    @property
    def can_go_back(self) -> bool:
        relative = self.current.relative_to(self.root)
        return bool(relative.parts)

    @property
    def header_path(self) -> str:
        relative = self.current.relative_to(self.root)
        paths = (self.root.parts[-1],) + relative.parts
        return "/".join(paths)
