from pathlib import Path

import magic
from django.http import HttpResponse
from django.http.request import HttpRequest
from django.shortcuts import render


def get_file_preview(file_path: Path) -> HttpResponse:
    with open(file_path, "r") as file:
        file_content = file.read()

        response = HttpResponse(
            file_content,
            content_type=magic.from_buffer(file_content),
        )
        response["Content-Disposition"] = "inline"

        return response


def get_list(
    request: HttpRequest,
    root: Path,
    current: Path,
    glob: str,
):
    files = current.glob(glob)

    return render(
        request,
        "django_explorer/list_plain.html",
        context={
            "root": root,
            "current": current,
            "files": files,
        },
    )
