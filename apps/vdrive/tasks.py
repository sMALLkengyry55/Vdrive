import logging
from datetime import time
import random
import time
import tempfile

from celery import shared_task
import urllib.request

from django.contrib.auth import get_user_model
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

from .scan import scan_gphotos, scan_gdrive
from .utils import get_google_credentials
from apps.vdrive.models import VideoProcessing, Video, VideoScan
from settings.base import RETRIABLE_STATUS_CODES, RETRIABLE_EXCEPTIONS, MAX_RETRIES


logger = logging.getLogger(__name__)
User = get_user_model()


def upload_to_youtube(file_descriptor, user):
    body = {"snippet": {"title": "title", "description": "desc", "categoryId": "22"},
            "status": {"privacyStatus": "unlisted"}
            }

    logger.debug(file_descriptor.name)
    credentials = get_google_credentials(user)
    youtube = build("youtube", "v3", credentials=credentials)
    insert_request = youtube.videos().insert(
                                            part=",".join(body.keys()),
                                            body=body,
                                            media_body=MediaFileUpload(file_descriptor.name,
                                                                       chunksize=-1,
                                                                       resumable=True))

    response = None
    error = None
    retry = 0
    while response is None:
        try:
            logger.info("Uploading file: %s", file_descriptor.name)
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    return response
                else:
                    raise ValueError("The upload failed with an unexpected response: %s" % response)
        except HttpError as er:
            if er.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (er.resp.status, er.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as er:
            error = "A retriable error occurred: %s" % er

        if error is not None:
            logger.debug(error)
            retry += 1
            if retry > MAX_RETRIES:
                raise ValueError("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            logger.debug("Sleeping %f seconds and then retrying...", sleep_seconds)
            time.sleep(sleep_seconds)


def download_from_drive(user, video_id, file_descriptor, video_processing):
    credentials = get_google_credentials(user)
    drive = build('drive', 'v3', credentials=credentials)
    request = drive.files().get_media(fileId=video_id)
    downloader = MediaIoBaseDownload(file_descriptor, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        video_processing.progress = int(status.progress() * 100)
        video_processing.save()
        logger.info("Download %d, %s." % (video_processing.progress, video_id))


def download_from_gphotos(user, video_id, file_descriptor, video_processing):
    credentials = get_google_credentials(user)
    photos = build('photoslibrary', 'v1', credentials=credentials)
    response = photos.mediaItems().get(mediaItemId=video_id).execute()
    base_url = response.get('baseUrl')
    if not base_url:
        raise ValueError('No video found')

    download_url = base_url + '=dv'

    with urllib.request.urlopen(download_url) as url_downloader:
        length = url_downloader.getheader('content-length')
        chunk_size = max(4096, int(length)//100)
        if not length:
            file_descriptor.write(url_downloader.read())
        else:
            while True:
                chunk = url_downloader.read(chunk_size)
                if not chunk:
                    break
                file_descriptor.write(chunk)


@shared_task
def process(video_processing_pk):
    video_processing = VideoProcessing.objects.get(pk=video_processing_pk)
    video = video_processing.video
    user = video.user
    video_id = video.source_id

    with tempfile.NamedTemporaryFile(mode='w+b', delete=True) as file_descriptor:
        print(f'Downloading {video_id} for {user}')
        if video_id is None:
            video_processing.status = VideoProcessing.Status.ERROR
            msg = 'No Id provided'
            video_processing.error_message_video = msg
            video_processing.save()
            raise ValueError(msg)

        video_processing.status = VideoProcessing.Status.DOWNLOAD
        video_processing.save()

        try:
            print(user, video_id, file_descriptor)
            if video_processing.video.source_type == Video.Type.GPHOTOS:
                download_from_gphotos(user, video_id, file_descriptor, video_processing)
            else:
                download_from_drive(user, video_id, file_descriptor, video_processing)

        except Exception as e:
            video_processing.status = VideoProcessing.Status.ERROR
            video_processing.error_message_video = f'Error: {e}'
            video_processing.save()
            raise
        video_processing.status = VideoProcessing.Status.UPLOAD
        video_processing.save()

        try:
            youtube_id = upload_to_youtube(file_descriptor, user)
            video_processing.video.youtube_id = youtube_id
            video_processing.save()
            video_processing.status = VideoProcessing.Status.SUCCESS
            video_processing.save()
        except HttpError as er:
            video_processing.status = VideoProcessing.Status.ERROR
            video_processing.error_message_video = f'An HTTP error occurred: {er.resp.status, er.content}'
            video_processing.save()
            raise


@shared_task
def scan_files(video_scan_id):
    video_scan = VideoScan.objects.get(id=video_scan_id)
    video_scan.status = VideoScan.Status.IN_PROGRESS
    video_scan.save()
    user = video_scan.user
    try:
        scan_gphotos(user)
        scan_gdrive(user)
    except Exception as e:
        video_scan.status = VideoScan.Status.ERROR
        video_scan.error_message = f'Error in scan: {e}'
        video_scan.save()

    video_scan.status = VideoScan.Status.SUCCESS
    video_scan.save()