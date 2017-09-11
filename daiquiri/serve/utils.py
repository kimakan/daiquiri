import os

from django.conf import settings

from daiquiri.query.utils import get_user_database_name
from daiquiri.core.adapter import get_adapter
from daiquiri.metadata.models import Database, Table, Column, Directory
from daiquiri.query.models import QueryJob


def get_columns(user, database_name, table_name):

    user_database_name = get_user_database_name(user)

    if database_name == user_database_name:
        # get the job fetch the columns
        try:
            job = QueryJob.objects.filter_by_owner(user).exclude(phase=QueryJob.PHASE_ARCHIVED).get(
                database_name=database_name,
                table_name=table_name
            )
            return job.metadata['columns']
        except QueryJob.DoesNotExist:
            return []

    else:
        # check permissions on the database
        try:
            database = Database.objects.filter_by_access_level(user).get(name=database_name)
        except Database.DoesNotExist:
            return []

        # check permissions on the table
        try:
            table = Table.objects.filter_by_access_level(user).filter(database=database).get(name=table_name)
        except Table.DoesNotExist:
            return []

        # get columns for this table
        return Column.objects.filter_by_access_level(user).filter(table=table).values()


def get_column(user, database_name, table_name, column_name):

    columns = get_columns(user, database_name, table_name)

    try:
        return [column for column in columns if column['name'] == column_name][0]
    except IndexError:
        # column_name is not in columns
        return None


def get_file(user, file_path):
    # append 'index.html' when the file_path is a directory
    if file_path.endswith('/'):
        file_path += 'index.html'

    # get directories this user has access to
    directories = Directory.objects.filter_by_access_level(user)

    results = set()
    for directory in directories:
        for directory_path, dirs, files in os.walk(directory.path):
            # normalize the file path so that /a/b/c and b/c/d/e become /a/b/c and d/e
            normalized_file_path = normalize_file_path(directory_path, file_path)

            # join directory_path and file_path so that it becomes /a/b/c/d/e
            absolute_file_path = os.path.join(directory_path, normalized_file_path)

            # check if absolute_file_path is actually a file
            if os.path.isfile(absolute_file_path):
                results.add(absolute_file_path)

    # check if we found the file more than once
    if len(results) > 1:
        raise Exception('More than one file found in %s.get_file().' % __name__)
    elif len(results) == 1:
        return results.pop()
    else:
        return None


def get_files(user, database_name, table_name, column_name):
    files = []

    if database_name and table_name and column_name:
        # get directories this user has access to
        directories = Directory.objects.filter_by_access_level(user)

        # get columns of this table the user is allowed to access
        column = get_column(user, database_name, table_name, column_name)
        if column:
            # get the filenames
            adapter = get_adapter()
            count = adapter.database.count_rows(database_name, table_name)
            rows = adapter.database.fetch_rows(database_name, table_name, [column['name']], page_size=count)

            for row in rows:
                for file_path in row:
                    for directory in directories:
                        file_path = normalize_file_path(directory.path, file_path)
                        if os.path.isfile(os.path.join(directory.path, file_path)):
                            files.append((directory.path, file_path))

    return files


def get_archive_file_name(user, table_name, column_name):
    if not user or user.is_anonymous():
        username = 'anonymous'
    else:
        username = user.username

    directory_name = os.path.join(settings.SERVE_DOWNLOAD_DIR, username)
    return os.path.join(directory_name, '%s_%s.zip' % (table_name, column_name))


def normalize_file_path(directory_path, file_path):

    directory_path_tokens = os.path.normpath(directory_path).split(os.path.sep)
    file_path_tokens = os.path.normpath(file_path).split(os.path.sep)

    match = 0
    for i in range(len(file_path_tokens)):
        if file_path_tokens[:i] == directory_path_tokens[-i:]:
            match = i

    return os.path.join(*file_path_tokens[match:])
