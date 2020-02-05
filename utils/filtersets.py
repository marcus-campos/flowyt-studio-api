from django_filters import rest_framework as rest_framework_filters
from django_filters.utils import try_dbfield


class BaseFilterSet(rest_framework_filters.FilterSet):
    @classmethod
    def filter_for_lookup(cls, field, lookup_type):
        DEFAULTS = dict(cls.FILTER_DEFAULTS)
        if hasattr(cls, "_meta"):
            DEFAULTS.update(cls._meta.filter_overrides)

        if hasattr(field, "enum_class"):
            data = try_dbfield(DEFAULTS.get, field.__class__) or {}
            filter_class = data.get("filter_class")
            params = data.get("extra", lambda field: {})(field)
            return filter_class, params
        return super().filter_for_lookup(field, lookup_type)
