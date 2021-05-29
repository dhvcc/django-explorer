from pathlib import Path

from django_explorer.templatetags.django_explorer import register
from django_explorer.templatetags.utils import sizeof_fmt


@register.simple_tag(takes_context=True)
def explorer_path(context: dict) -> str:
    relative = context["current"].relative_to(context["root"])
    path = (context["root"].parts[-1],) + relative.parts
    return "/".join(path)


@register.simple_tag(takes_context=True)
def can_go_back(context: dict) -> bool:
    relative = context["current"].relative_to(context["root"])
    return bool(relative.parts)


@register.simple_tag
def file_href(file: Path) -> str:
    return f"href={file.parts[-1]}"


@register.simple_tag
def file_name(file: Path) -> str:
    icon = "📁" if file.is_dir() else "🗎"
    return f"{icon} {file.name}"


@register.simple_tag
def file_size(file: Path) -> str:
    return sizeof_fmt(file.stat().st_size)
