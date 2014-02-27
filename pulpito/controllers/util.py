from datetime import timedelta


def set_job_status_class(job):
    status_class_map = {
        'pass':    'success',
        'fail':    'danger',
        'dead':    'danger',
        'running': 'warning',
        'unknown': 'warning',
        None:      'warning',
    }

    job['status_class'] = status_class_map.get(job.get('status', 'unknown'))


def set_job_time_info(job):
    job['posted_pretty'] = job['posted'].split('.')[0]
    job['updated_pretty'] = job['updated'].split('.')[0]
    duration = job.get('duration')
    if duration:
        duration_pretty = str(timedelta(seconds=job['duration']))
        job['duration_pretty'] = duration_pretty


def prettify_job(job):
    set_job_status_class(job)
    set_job_time_info(job)
    return job


def get_run_filters(**kwargs):
    filters = dict()
    for (key, value) in kwargs.iteritems():
        if value == '':
            continue
        elif key == 'latest':
            continue
        else:
            filters[key] = value
    return filters
