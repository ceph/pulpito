from datetime import datetime, timedelta
from ..filters import utc_stamp_to_local

timestamp_fmt = '%Y-%m-%d %H:%M:%S'

status_class_map = {
    'pass':    'success',
    'fail':    'danger',
    'dead':    'danger',
    'running': 'warning',
    'unknown': 'warning',
    None:      'warning',
}


def remove_msecs(timestamp):
    return timestamp.split('.')[0]


def prettify_run(run):
    set_run_status_class(run)
    set_run_time_info(run)


def set_run_status_class(run):
    for key in status_class_map.keys():
        if key and key in run.get('status', 'unknown'):
            status_class = status_class_map[key]
            run['status_class'] = status_class
            break


def set_run_time_info(run):
    if 'posted' in run:
        run['posted'] = remove_msecs(run['posted'])
    if 'running' in run.get('status', ''):
        posted_local = utc_stamp_to_local(run['posted'])
        posted = datetime.strptime(posted_local, timestamp_fmt)
        run['runtime'] = remove_msecs(str(datetime.now() - posted))
    if 'scheduled' in run:
        run['scheduled'] = remove_msecs(run['scheduled'])


def prettify_job(job):
    set_job_status_class(job)
    set_job_time_info(job)
    return job


def set_job_status_class(job):
    job['status_class'] = status_class_map.get(job.get('status', 'unknown'))


def set_job_time_info(job):
    if 'posted' in job:
        job['posted_pretty'] = remove_msecs(job['posted'])
        posted = datetime.strptime(job['posted_pretty'], timestamp_fmt)
    if 'updated' in job:
        job['updated_pretty'] = remove_msecs(job['updated'])
        updated = datetime.strptime(job['updated_pretty'], timestamp_fmt)
    if 'posted' in job and 'updated' in job:
        if job['status'] == 'running':
            job['runtime'] = remove_msecs(str(datetime.utcnow() - posted))
        else:
            job['runtime'] = str(updated - posted)
    if job.get('duration'):
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
