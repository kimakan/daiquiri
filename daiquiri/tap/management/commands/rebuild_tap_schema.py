from django.core.management.base import BaseCommand

from daiquiri.metadata.models import Schema
from daiquiri.tap.models import (
    Schema as TapSchema,
    Table as TapTable,
    Column as TapColumn,
)
from daiquiri.tap.utils import update_schema


class Command(BaseCommand):

    def handle(self, *args, **options):

        TapSchema.objects.all().delete()
        TapTable.objects.all().delete()
        TapColumn.objects.all().delete()

        for schema in Schema.objects.all():
            update_schema(schema)
