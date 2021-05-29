from django.conf import settings

from django_explorer import types


def get_explorer_settings() -> types.ExplorerSettings:
    default_settings = types.ExplorerSettings().dict()
    user_settings = getattr(settings, "EXPLORER_SETTINGS", {})
    return types.ExplorerSettings(
        **{
            **default_settings,
            **user_settings,
        }
    )
