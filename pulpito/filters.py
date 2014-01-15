import jinja2.filters
import json


def tojson_filter(obj, **kwargs):
    return jinja2.Markup(json.dumps(obj, **kwargs))


def setup_filters():
    if not 'tojson' in jinja2.filters.FILTERS:
        jinja2.filters.FILTERS['tojson'] = tojson_filter
        return True
    return False
