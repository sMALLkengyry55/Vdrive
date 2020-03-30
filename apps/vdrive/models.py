from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Video(models.Model):
    class Meta:
        ordering = ['-id']

    class Type(models.TextChoices):
        GDRIVE = 'Google Drive', _('Gdrive type')
        GPHOTOS = 'Google Photos', _('Gphotos type')

    class Status(models.TextChoices):
        ONDRIVE = 'waiting on drive', _('Waiting to upload')
        DELETED = 'deleted', _('Successfully deleted')

    status = models.CharField(max_length=50, choices=Status.choices, default=Status.ONDRIVE)
    source_id = models.CharField(verbose_name=_(" id of video in the source"), max_length=250)
    name = models.CharField(verbose_name=_("name of the video"), max_length=250)
    source_type = models.CharField(choices=Type.choices, verbose_name=_("source of the file"), max_length=250)
    user = models.ForeignKey(get_user_model(), related_name='videos', on_delete=models.CASCADE)
    youtube_id = models.CharField(verbose_name=_("id of youtube uploaded video"), max_length=250, blank=True)
    thumbnail = models.URLField(verbose_name=_("thumbnail of the video"), max_length=1000)
    size = models.CharField(verbose_name=_("File size"), max_length=250)


class Processing(models.Model):
    class Meta:
        ordering = ['-date']
    date = models.DateTimeField(verbose_name=_("creation date"), auto_now_add=True, null=True)


class VideoProcessing(models.Model):
    class Status(models.TextChoices):
        WAITING = 'waiting', _('Waiting to upload')
        DOWNLOAD = 'download', _('Download')
        UPLOAD = 'uploading', _('In progress of uploading')
        ERROR = 'errors', _('Error message')
        SUCCESS = 'success', _('Successfully Uploaded')

    processing = models.ForeignKey('Processing', on_delete=models.CASCADE,  related_name='videos')
    video = models.ForeignKey('Video', on_delete=models.CASCADE, related_name='processings')
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.WAITING)
    error_message_video = models.TextField(blank=True)

    @property
    def youtube_link(self):
        return 'youtu.be/aaaa'


class VideoScan(models.Model):
    class Status(models.TextChoices):
        WAITING = 'waiting', _('Waiting to scan')
        IN_PROGRESS = 'in_progress', _('Scanning')
        SUCCESS = 'success', _('Success')
        ERROR = 'error', _('Error')

    user = models.ForeignKey(get_user_model(), related_name='video_scans', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name=_("Date"), auto_now_add=True)
    status = models.CharField(max_length=50, choices=Status.choices, default=Status.WAITING)
    error_message = models.TextField(_('Error'), blank=True)