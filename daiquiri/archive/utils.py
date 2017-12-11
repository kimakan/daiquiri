import os

from django.conf import settings


def get_download_file_name(user, task_id):
    if not user or user.is_anonymous():
        username = 'anonymous'
    else:
        username = user.username

    directory_name = os.path.join(settings.ARCHIVE_DOWNLOAD_DIR, username)
    return os.path.join(directory_name, task_id + '.zip')
