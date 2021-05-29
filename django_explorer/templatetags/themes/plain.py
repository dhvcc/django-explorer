from pathlib import Path

from django_explorer.templatetags.django_explorer import register
from django_explorer.templatetags.utils import sizeof_fmt
from django_explorer.types import TemplateContext


@register.simple_tag(takes_context=True)
@TemplateContext.validate
def explorer_path(context: TemplateContext) -> str:
    relative = context.current.relative_to(context.root)
    paths = (context.root.parts[-1],) + relative.parts
    return "/".join(paths)


@register.simple_tag(takes_context=True)
@TemplateContext.validate
def can_go_back(context: TemplateContext) -> bool:
    relative = context.current.relative_to(context.root)
    return bool(relative.parts)


@register.simple_tag(takes_context=True)
@TemplateContext.validate
def file_href(context: TemplateContext, file: Path) -> str:
    request = context.request
    paths = [request.path.lstrip("/"), file.parts[-1]]
    return "href={}".format("/".join(paths))


@register.simple_tag
def file_name(file: Path) -> str:
    icon = "📁" if file.is_dir() else "🗎"
    return f"{icon} {file.name}"


@register.simple_tag
def file_size(file: Path) -> str:
    return sizeof_fmt(file.stat().st_size)
