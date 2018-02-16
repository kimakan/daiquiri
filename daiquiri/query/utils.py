import sys

from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from daiquiri.core.adapter import DatabaseAdapter
from daiquiri.core.utils import human2bytes
from daiquiri.metadata.models import Schema, Table, Column, Function


def get_format_config(format_key):
    return [f for f in settings.QUERY_DOWNLOAD_FORMATS if f['key'] == format_key][0]


def get_default_table_name():
    return now().strftime("%Y-%m-%d-%H-%M-%S")


def get_default_queue():
    return settings.QUERY_QUEUES[0]['key']


def get_query_language_choices():
    return [('%(key)s-%(version)s' % item, item['label']) for item in settings.QUERY_LANGUAGES]


def get_queue_choices():
    return [(item['key'], item['label']) for item in settings.QUERY_QUEUES]


def get_user_schema_name(user):
    if not user or user.is_anonymous():
        username = 'anonymous'
    else:
        username = user.username

    return settings.QUERY_USER_SCHEMA_PREFIX + username


def get_quota(user):
    if not user or user.is_anonymous():
        anonymous_quota = human2bytes(settings.QUERY_QUOTA.get('anonymous'))
        return anonymous_quota if anonymous_quota else 0

    else:
        user_quota = human2bytes(settings.QUERY_QUOTA.get('user'))
        quota = user_quota if user_quota else 0

        # apply quota for user
        user_quotas = settings.QUERY_QUOTA.get('users')
        if user_quotas:
            user_quota = human2bytes(user_quotas.get(user.username))
            if user_quota:
                quota = user_quota if user_quota > quota else quota

        # apply quota for group
        group_quotas = settings.QUERY_QUOTA.get('groups')
        if group_quotas:
            for group in user.groups.all():
                group_quota = human2bytes(group_quotas.get(group.name))
                if group_quota:
                    quota = group_quota if group_quota > quota else quota

    return quota


def fetch_user_schema_metadata(user, jobs):

    schema_name = get_user_schema_name(user)

    schema = {
        'order': sys.maxsize,
        'name': schema_name,
        'query_strings': [schema_name],
        'description': _('Your personal schema'),
        'tables': []
    }

    for job in jobs:
        if job.phase == job.PHASE_COMPLETED:
            table = {
                'name': job.table_name,
                'query_strings': [schema_name, job.table_name],
                'columns': job.metadata['columns']
            }

            for column in table['columns']:
                column['query_strings'] = [column['name']]

            schema['tables'].append(table)

    return [schema]


def get_asterisk_columns(display_column):
    schema_name, table_name, _ = display_column[1]
    column_names = DatabaseAdapter().fetch_column_names(schema_name, table_name)
    return [(column_name, (schema_name, table_name, column_name)) for column_name in column_names]


def check_permissions(user, keywords, tables, columns, functions):
    messages = []

    # check keywords against whitelist
    for keywords in keywords:
        pass

    if not settings.METADATA_COLUMN_PERMISSIONS:
        # check permissions on schemas/tables
        for schema_name, table_name in tables:
            # check permission on schema
            if schema_name in [None, settings.TAP_SCHEMA, get_user_schema_name(user)]:
                continue
            else:
                try:
                    schema = Schema.objects.filter_by_access_level(user).get(name=schema_name)
                except Schema.DoesNotExist:
                    messages.append(_('Schema %s not found.') % schema_name)
                    continue

            # check permission on table
            if table_name is None:
                continue
            else:
                try:
                    Table.objects.filter_by_access_level(user).filter(schema=schema).get(name=table_name)
                except Table.DoesNotExist:
                    messages.append(_('Table %s not found.') % table_name)
                    continue

    else:
        # check permissions on schemas/tables/columns
        for column in columns:
            schema_name, table_name, column_name = column

            # check permission on schema
            if schema_name in [None, settings.TAP_SCHEMA, get_user_schema_name(user)]:
                continue
            else:
                try:
                    schema = Schema.objects.filter_by_access_level(user).get(name=schema_name)
                except Schema.DoesNotExist:
                    messages.append(_('Schema %s not found.') % schema_name)
                    continue

            # check permission on table
            if table_name is None:
                continue
            else:
                try:
                    table = Table.objects.filter_by_access_level(user).filter(schema=schema).get(name=table_name)
                except Table.DoesNotExist:
                    messages.append(_('Table %s not found.') % table_name)
                    continue

            # check permission on column
            if column_name is None:
                continue
            elif column_name == '*':
                columns = Column.objects.filter_by_access_level(user).filter(table=table)
                actual_columns = DatabaseAdapter().fetch_columns(schema_name, table_name)

                column_names_set = set([column.name for column in columns])
                actual_column_names_set = set([column['name'] for column in actual_columns])

                if column_names_set != actual_column_names_set:
                    messages.append(_('The asterisk (*) is not allowed for this table.'))
                    continue
            else:
                try:
                    column = Column.objects.filter_by_access_level(user).filter(table=table).get(name=column_name)
                except Column.DoesNotExist:
                    messages.append(_('Column %s not found.') % column_name)
                    continue

    # check permissions on functions
    for function_name in functions:
        if function_name.upper() in DatabaseAdapter().FUNCTIONS:
            continue
        else:
            # check permission on function
            try:
                Function.objects.filter_by_access_level(user).get(name=function_name)
            except Function.DoesNotExist:
                messages.append(_('Function %s not found.') % function_name)
                continue

    # return the error stack
    return list(set(messages))
