from enum import Enum

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
