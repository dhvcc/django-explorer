from enum import Enum
from typing import TypedDict, Union


class ExplorerTheme(Enum):
    plain = "plain"
    vue = "vue"


class ExplorerSettings(TypedDict):
    theme: Union[ExplorerTheme, str]
