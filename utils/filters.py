import json

from django_filters import rest_framework as rest_framework_filters
from django_filters.constants import EMPTY_VALUES


class JSONFilter(rest_framework_filters.Filter):
    def filter(self, qs, value):
        if value in EMPTY_VALUES:
            return qs

        filter_params = json.loads(value)
        return qs.filter(**filter_params)

        # params = {}
        # for k,v in dict_value.items():
        #     key = "%s__%s"%(self.field_name, k)
        #     params[key]=v
        #
        # return qs.filter(**params)
