import json
import logging
import datetime

import requests
from googleapiclient.discovery import build
import urllib.request
from hurry.filesize import size as sizer

from apps.vdrive.models import VideoProcessing, Processing, Video, VideoScan
from .utils import get_google_credentials


logger = logging.getLogger(__name__)


def scan_gdrive(user):
    drive = build('drive', 'v3', credentials=get_google_credentials(user))
    files_data = drive.files().list(q="mimeType contains 'video/'",
                                    spaces='drive',
                                    fields='files(id, name, size, thumbnailLink)'
                                    ).execute()
    logger.info(f'Found fies {files_data}')

    for item in files_data["files"]:
        video = Video.objects.get_or_create(source_type=Video.Type.GDRIVE,
                                            source_id=item['id'],
                                            user=user,
                                            defaults={
                                                'name': item['name'],
                                                'size': sizer(int(item['size'])),
                                                'thumbnail': item['thumbnailLink'],
                                            })
    return files_data['files']


def get_gphotos(user):
    creds = get_google_credentials(user)
    url = 'https://photoslibrary.googleapis.com/v1/mediaItems:search'
    payload = {
        'filters': {"mediaTypeFilter": {"mediaTypes": ['VIDEO', ]}}
    }

    last_successfull_scan = user.video_scans.filter(status=VideoScan.Status.SUCCESS).last()
    if last_successfull_scan:
        start = last_successfull_scan.date - datetime.timedelta(days=1)
        end = datetime.datetime.now() + datetime.timedelta(days=1)
        payload['filters']['dateFilter']['ranges'] = [
            {
                "startDate": {
                        "year": start.year,
                        "month": start.month,
                        "day": start.day
                },
                "endDate": {
                    "year": end.year,
                    "month": end.month,
                    "day": end.day
                }
            },
        ]
    headers = {
        'content-type': 'application/json',
        'Authorization': f'Bearer {creds.token}'
    }

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code != 200:
        raise ValueError('Failed to retrieve data from gphotos')

    results = response.json()
    for video in results.get('mediaItems', []):
        yield video

    while results.get('nextPageToken', None):
        payload['pageToken'] = results.get('nextPageToken')
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(response)
        print(response.json())
        if response.status_code != 200:
            raise ValueError('Failed to retrieve data from gphotos')

        results = response.json()
        for video in results.get('mediaItems', []):
            yield video


def scan_gphotos(user):
    for item in get_gphotos(user):
        base_url = item.get('baseUrl')

        if not base_url:
            logger.error(f'No base url for video {item}')
            continue

        download_url = base_url + '=dv'
        size = 0

        try:
            with urllib.request.urlopen(download_url) as url_downloader:
                size = sizer(int(url_downloader.getheader('content-length')))

        except Exception:
            logger.error(f'Error fetching size for video {item}')

        Video.objects.get_or_create(source_type=Video.Type.GPHOTOS,
                                    source_id=item['id'],
                                    user=user,
                                    defaults={
                                        'thumbnail': base_url + '=w300-h200',
                                        'name': item.get('filename', 'UNKNOWN'),
                                        'size': size,
                                    })