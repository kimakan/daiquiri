from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from daiquiri.core.utils import import_class, make_query_dict_upper_case


def CutOutAdapter():
    return import_class(settings.CUTOUT_ADAPTER)()


class BaseCutOutAdapter(object):

    def clean(self, request, resource):
        raise NotImplementedError()

    def stream(self):
        raise NotImplementedError()

    def parse_query_dict(self, request):
        data = make_query_dict_upper_case(request.GET)

        args = {}
        errors = {}
        for key in self.keys:
            try:
                value = float(data[key])

                if self.ranges[key]['min'] <= value <= self.ranges[key]['max']:
                    args[key] = value
                else:
                    errors[key] = [_('This value must be between %(min)g and %(max)g.' % self.ranges[key])]

            except KeyError:
                if key in self.defaults:
                    args[key] = self.defaults[key]
                else:
                    errors[key] = [_('This field may not be blank.')]

            except ValueError:
                errors[key] = [_('This field must be a float.')]

        return args, errors
