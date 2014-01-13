from datetime import timedelta


def get_job_status_class(job):
    status_class_map = {
        'pass':    'success',
        'fail':    'danger',
        'dead':    'danger',
        'running': 'warning',
        'unknown': 'warning',
        None:      'warning',
    }
    return status_class_map.get(job.get('status', 'unknown'))


def get_job_time_info(job):
    duration = job.get('duration')
    if duration:
        duration_pretty = str(timedelta(seconds=job['duration']))
        return duration_pretty


def get_run_filters(**kwargs):
    filters = dict()
    for (key, value) in kwargs.iteritems():
        if value == '':
            continue
        elif key == 'latest' and value is False:
            continue
        else:
            filters[key] = value
    return filters
