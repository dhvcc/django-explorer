from typing import Callable, List, Optional, Sequence

import magic
from django.conf.urls import include
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls.conf import re_path
from django.views import View

from django_explorer.signals import file_download
from django_explorer.types import ExplorerContext, ExplorerFile


class BaseExplorerView(View):
    http_method_names = ("get",)
    fields = "__all__"

    root: str
    permissions: List[Callable] = []  # TODO: DRF compatible
    filters: List[Callable] = []

    go_back_url: Optional[str] = None
    glob: str = "*"

    @classmethod
    def as_view(cls, **initkwargs):
        view = super().as_view(**initkwargs)
        view.cls = cls
        view.initkwargs = initkwargs

        return view

    @classmethod
    def as_include(cls, *, reverse_name: Optional[str] = None, **initkwargs):
        urlpatterns = [
            re_path(r"(?P<relative>.*)", cls.as_view(**initkwargs), name=reverse_name),
        ]
        return include(urlpatterns)

    def get(self, relative: str):
        for permission in self.permissions:
            can_forward = permission(self.request.user)
            if not can_forward:
                return HttpResponse(status=403)
        if "list" in self.request.GET:
            return self.list()
        elif "preview" in self.request.GET:
            return self.preview()
        elif "download" in self.request.GET:
            return self.download()
        return HttpResponse("Test")

    def list(self, context: ExplorerContext):
        glob_results = context.current.glob(self.glob)

        return render(
            request,
            "django_explorer/list_plain.html",
            context={
                "root": context.root,
                "current": context.current,
                "files": [ExplorerFile.from_path(path, self.request) for path in glob_results],
            },
        )

    def fallback(self, request):
        pass

    @staticmethod
    def file_response_base(file_path: str):
        with open(file_path, "r") as file:
            file_content = file.read()

            response = HttpResponse(
                file_content,
                content_type=magic.from_buffer(file_content),
            )

        return response

    def preview(self, context: ExplorerContext):
        response = self.file_response_base(context.current)
        response["Content-Disposition"] = "inline"
        return response

    def download(self, context: ExplorerContext):
        response = self.file_response_base()
        response["Content-Disposition"] = "attachment"
        file_download.send(
            sender=self.__class__.__name__,
            request=self.request,
            file=context.current,
        )
        return response

    def get_fields(self) -> Sequence[str]:
        if self.fields == "__all__":
            return ("fname", "size", "download")
        return self.fields
