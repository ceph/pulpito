from datetime import datetime, timedelta

timestamp_fmt = '%Y-%m-%d %H:%M:%S'

run_status_map = {
    'pass':    'success',
    'fail':    'danger',
    'dead':    'danger',
    'running': 'warning',
    'unknown': 'warning',
    None:      'warning',
    'waiting': 'info',
}


def remove_msecs(timestamp):
    return timestamp.split('.')[0]


def remove_delta_msecs(delta):
    return delta - timedelta(microseconds=getattr(delta, 'microseconds', 0))


def prettify_run(run):
    set_run_status_class(run)
    set_run_time_info(run)
    set_run_wait_time(run)


def set_run_wait_time(run):
    if run.get('jobs'):
        total_wait_time = None
        for job in run['jobs']:
            if job.get("wait_time"):
                if total_wait_time:
                    total_wait_time = total_wait_time + job['wait_time']
                else:
                    total_wait_time = job['wait_time']

        if total_wait_time:
            run["total_wait_time"] = total_wait_time
            jobs_that_waited = [job for job in run['jobs']
                                if job.get("wait_time")]
            run["avg_wait_time"] = remove_delta_msecs(
                total_wait_time / len(jobs_that_waited)
            )


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
        if run['status'] in ['running', 'waiting']:
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
    remove_none_strings(job)
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
        if job['status'] in ['running', 'waiting']:
            job['runtime'] = remove_delta_msecs(datetime.utcnow() - started)
        else:
            updated = datetime.strptime(job['updated'], timestamp_fmt)
            job['runtime'] = remove_delta_msecs(updated - started)
    # The duration has to be reported by teuthology internal.timer task
    # when unwinding, however, there are other task are starting before
    # the timer, so if one of them fails, the duration will not appear
    # in summary.yaml and won't be reported to paddles.
    # From other side, the 'runtime' which is calculated above using
    # 'started' and 'updated' timestamp, but it can also happen that
    # the 'started' timestamp is not reported, correspondingly we
    # cannot calculate 'runtime' and 'wait_time'.
    duration = job.get('duration')
    runtime = job.get('runtime')
    if duration:
        duration_delta = timedelta(seconds=duration)
        job['duration'] = str(duration_delta)

    if duration and runtime:
        duration_delta = timedelta(seconds=duration)
        job['wait_time'] = remove_delta_msecs(runtime - duration_delta)
    elif job.get("status") == 'waiting':
        job['wait_time'] = runtime


def remove_none_strings(obj):
    for key, value in obj.items():
        if str(value) == 'None':
            obj[key] = ''
    return obj


def get_run_filters(**kwargs):
    filters = dict()
    for (key, value) in kwargs.items():
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
