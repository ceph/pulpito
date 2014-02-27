import jinja2.filters
import json
import calendar
from datetime import datetime


def tojson_filter(obj, **kwargs):
    return jinja2.Markup(json.dumps(obj, **kwargs))


def utc_stamp_to_local(stamp, format='%Y-%m-%d %H:%M:%S'):
    utc_dt = datetime.strptime(stamp, format)
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    return local_dt.strftime(format)


def setup_filters():
    jinja2.filters.FILTERS['localtime'] = utc_stamp_to_local
    if not 'tojson' in jinja2.filters.FILTERS:
        jinja2.filters.FILTERS['tojson'] = tojson_filter
    return True
