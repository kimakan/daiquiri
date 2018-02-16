import logging

from .base import DownloadAdapter

logger = logging.getLogger(__name__)


class MysqldumpAdapter(DownloadAdapter):

    FORMATS = {
        'char': 'c',
        'unsignedByte': 'B',
        'short': 'h',
        'int': 'i',
        'long': 'q',
        'float': 'f',
        'double': 'd'
    }

    NULL_VALUES = {
        'char': '',
        'unsignedByte': 255,
        'short': 32767,
        'int': 2147483647,
        'long': 9223372036854775807,
        'float': float('nan'),
        'double': float('nan')
    }

    def set_args(self, schema_name, table_name):
        self.args = ['mysqldump', '--compact', '--skip-extended-insert']

        if 'USER' in self.database_config and self.database_config['USER']:
            self.args.append('--user=%(USER)s' % self.database_config)

        if 'PASSWORD' in self.database_config and self.database_config['PASSWORD']:
            self.args.append('--password=%(PASSWORD)s' % self.database_config)

        if 'HOST' in self.database_config and self.database_config['HOST']:
            self.args.append('--host=%(HOST)s' % self.database_config)

        if 'PORT' in self.database_config and self.database_config['PORT']:
            self.args.append('--port=%(PORT)s' % self.database_config)

        self.args.append(schema_name)
        self.args.append(table_name)
