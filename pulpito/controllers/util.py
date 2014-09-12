from datetime import datetime, timedelta
from ..filters import utc_stamp_to_local

timestamp_fmt = '%Y-%m-%d %H:%M:%S'

run_status_map = {
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
    for key in run_status_map.keys():
        if key and key in run.get('status', 'unknown'):
            status_class = run_status_map[key]
            run['status_class'] = status_class
            break


def set_run_time_info(run):
    if run.get('scheduled'):
        run['scheduled'] = remove_msecs(run['scheduled'])
    if run.get('posted'):
        run['posted'] = remove_msecs(run['posted'])
    if run.get('updated'):
        run['updated'] = remove_msecs(run['updated'])
    if run.get('started'):
        run['started'] = remove_msecs(run['started'])
        started = datetime.strptime(run['started'], timestamp_fmt)
        if run['status'] == 'running':
            run['runtime'] = remove_msecs(str(datetime.utcnow() - started))
        else:
            run_updated = run.get('updated', run['posted'])
            if not run_updated:
                run['runtime'] = ''
            else:
                updated = datetime.strptime(run_updated, timestamp_fmt)
                run['runtime'] = remove_msecs(str(updated - started))


def prettify_job(job):
    set_job_status_class(job)
    set_job_time_info(job)
    return job


def set_job_status_class(job):
    job['status_class'] = run_status_map.get(job.get('status', 'unknown'))


def set_job_time_info(job):
    if job.get('posted'):
        job['posted'] = remove_msecs(job['posted'])
    if job.get('started'):
        job['started'] = remove_msecs(job['started'])
    if job.get('updated'):
        job['updated'] = remove_msecs(job['updated'])
    if job.get('started') and job.get('updated'):
        started = datetime.strptime(job['started'], timestamp_fmt)
        if job['status'] == 'running':
            job['runtime'] = remove_msecs(str(datetime.utcnow() - started))
        else:
            updated = datetime.strptime(job['updated'], timestamp_fmt)
            job['runtime'] = str(updated - started)
    if job.get('duration'):
        duration = str(timedelta(seconds=job['duration']))
        job['duration'] = duration


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


def set_node_status_class(node):
    up = node.get('up')
    locked = node.get('locked')
    if up is True and locked is False:
        status_class = 'success'
    elif up is False:
        status_class = 'danger'
    elif locked is True:
        status_class = 'warning'
    else:
        status_class = ''
    node['status_class'] = status_class
