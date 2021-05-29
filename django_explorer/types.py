import functools
from enum import Enum
from pathlib import Path

from django.http import HttpRequest
from django.template.context import RequestContext
from pydantic import BaseModel


class ExplorerTheme(Enum):
    plain = "plain"
    admin = "admin"
    vue = "vue"


class ExplorerSettings(BaseModel):
    theme: ExplorerTheme = ExplorerTheme.plain.value
    glob: str = "*"

    class Config:
        use_enum_values = True


class TemplateContext(BaseModel):
    request: HttpRequest
    root: Path
    current: Path

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def validate(function):
        @functools.wraps(function)
        def wrapper(context: RequestContext, *args, **kwargs):
            return function(TemplateContext(**context.flatten()), *args, **kwargs)

        return wrapper
