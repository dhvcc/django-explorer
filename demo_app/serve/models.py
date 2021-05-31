from pathlib import Path

from django.contrib import admin
from django.db import models
from django.dispatch import receiver
from django.http import HttpRequest

from django_explorer.signals import file_download


class Download(models.Model):
    file = models.CharField(max_length=255, editable=False)
    when = models.DateTimeField(auto_now=True, editable=False)
    user = models.CharField(max_length=255, editable=False)


@admin.register(Download)
class DownloadAdmin(admin.ModelAdmin):
    readonly_fields = (
        "file",
        "when",
        "user",
    )


@receiver(file_download)
def file_download_receiver(sender, request: HttpRequest, file: Path, **kwargs):
    Download.objects.create(
        file=file, user="Anonymus" if not request.user.is_authenticated else request.user.username
    )
