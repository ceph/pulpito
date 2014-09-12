import jinja2.filters
import json
from datetime import datetime
import pytz
import tzlocal


local_tz = tzlocal.get_localzone()


def tojson_filter(obj, **kwargs):
    return jinja2.Markup(json.dumps(obj, **kwargs))


def brief_filter(obj, **kwargs):
    if obj in (None, 'None'):
        return ''
    return obj


def utc_stamp_to_local(stamp, format='%Y-%m-%d %H:%M:%S'):
    if not stamp:
        return ''
    utc_dt_naive = datetime.strptime(stamp, format)
    utc_dt_aware = pytz.utc.localize(utc_dt_naive)
    local_dt = utc_dt_aware.astimezone(local_tz)
    return local_dt.strftime(format)


def setup_filters():
    jinja2.filters.FILTERS['localtime'] = utc_stamp_to_local
    if 'tojson' not in jinja2.filters.FILTERS:
        jinja2.filters.FILTERS['tojson'] = tojson_filter
    if 'brief' not in jinja2.filters.FILTERS:
        jinja2.filters.FILTERS['brief'] = brief_filter
    return True
