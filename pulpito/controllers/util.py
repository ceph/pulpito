from datetime import datetime, timedelta
from ..filters import utc_stamp_to_local

timestamp_fmt = '%Y-%m-%d %H:%M:%S'


def prettify_run(run):
    set_run_status_class(run)
    set_run_time_info(run)


def set_run_status_class(run):
    fail = run['results']['fail']
    running = run['results']['running']
    passing = run['results']['pass']
    status_class = 'warning'
    if fail:
        status_class = 'danger'
    elif not running and passing:
        status_class = 'success'
    elif running and passing:
        status_class = 'warning'
    else:
        status_class = 'warning'
    run['status_class'] = status_class


def set_run_time_info(run):
    run['posted'] = run['posted'].split('.')[0]
    if 'running' in run['status']:
        posted_local = utc_stamp_to_local(run['posted'])
        posted = datetime.strptime(posted_local, timestamp_fmt)
        run['runtime'] = str(datetime.now() - posted).split('.')[0]


def prettify_job(job):
    set_job_status_class(job)
    set_job_time_info(job)
    return job


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
    posted = datetime.strptime(job['posted_pretty'], timestamp_fmt)
    updated = datetime.strptime(job['updated_pretty'], timestamp_fmt)
    job['runtime'] = str(updated - posted)
    duration = job.get('duration')
    if duration:
        duration_pretty = str(timedelta(seconds=job['duration']))
        job['duration_pretty'] = duration_pretty


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
