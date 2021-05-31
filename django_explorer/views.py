import os
from typing import Callable, List, Optional, Sequence

import magic
from django.conf.urls import include
from django.http.response import HttpResponse
from django.shortcuts import render
from django.urls.conf import re_path
from django.views import View

from django_explorer.signals import file_download
from django_explorer.types import ExplorerContext, ExplorerFile


class BaseExplorerView(View):
    http_method_names = ("get",)
    fields = "__all__"

    root: str = ""
    permissions: List[Callable] = []  # TODO: DRF compatible
    filters: List[Callable] = []

    go_back_url: Optional[str] = None
    glob: str = "*"

    template_name: str

    @classmethod
    def as_view(cls, **initkwargs):
        root = initkwargs["root"]

        if not root.exists():
            raise ValueError("root argument path does not exist")
        if not root.is_dir():
            raise ValueError("root argument path should be a directory")

        view = super().as_view(**initkwargs)

        view.cls = cls
        view.initkwargs = initkwargs

        return view

    @classmethod
    def as_include(cls, *, reverse_name: Optional[str] = None, **initkwargs):
        view = cls.as_view(**initkwargs)

        urlpatterns = [
            re_path(r"(?P<relative>.*)", view, name=reverse_name),
        ]
        return include(urlpatterns)

    def get(self, request, relative: str):
        for permission in self.permissions:
            valid_user = permission(self.request.user)
            if not valid_user:
                return HttpResponse(status=403)

        context = ExplorerContext.from_relative(self.root, relative)

        print(context.current, context.current.exists())
        if not context.current.exists():
            return self.fallback("Path does not exist", 404)

        if context.current.is_dir():
            return self.list(context)

        if "download" in request.GET:
            return self.download(context)
        return self.preview(context)

    def get_list_render_context(self, context: ExplorerContext, glob_results):
        directories = []
        files = []

        for path in glob_results:
            e_file = ExplorerFile.from_path(path, self.request)
            if os.path.isdir(path):
                directories.append(e_file)
            elif os.path.isfile(path):
                files.append(e_file)

        # Directories first and sort array's by path.name
        result_files = [*sorted(directories), *sorted(files)]

        return {
            "root": context.root,
            "header_path": context.header_path,
            "can_go_back": context.can_go_back,
            "current": context.current,
            "files": result_files,
        }

    def list(self, context: ExplorerContext):
        glob_results = context.current.glob(self.glob)

        return render(
            self.request,
            self.template_name,
            context=self.get_list_render_context(context, glob_results),
        )

    def fallback(self, message="Error", status: int = 400):
        return HttpResponse(message, status=status)

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
        if not context.current.is_file():
            return self.fallback()

        response = self.file_response_base(context.current)
        response["Content-Disposition"] = "inline"
        return response

    def download(self, context: ExplorerContext):
        if not context.current.is_file():
            return self.fallback()

        response = self.file_response_base(context.current)
        response["Content-Disposition"] = "attachment"
        file_download.send(
            sender=self.__class__.__name__,
            request=self.request,
            file=context.relative,
        )
        return response

    def get_fields(self) -> Sequence[str]:
        if self.fields == "__all__":
            return ("fname", "size", "download")
        return self.fields


class PlainExplorerView(BaseExplorerView):
    template_name = "django_explorer/list_plain.html"
