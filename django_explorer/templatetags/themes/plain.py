from django_explorer.templatetags.django_explorer import register
from django_explorer.types import ExplorerFile


@register.simple_tag
def plain_file_name(file: ExplorerFile) -> str:
    icon = "📁" if file.type == "directory" else "🗎"
    return f"{icon} {file.path.name}"
