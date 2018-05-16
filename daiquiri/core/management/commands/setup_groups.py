from django.core.management.base import BaseCommand

from daiquiri.core.constants import GROUPS
from daiquiri.core.utils import setup_group


class Command(BaseCommand):

    def handle(self, *args, **options):

        for name in GROUPS:
            group, created = setup_group(name)

            if created:
                print ('Group "%s" created' % name)
            else:
                print ('Group "%s" updated' % name)
