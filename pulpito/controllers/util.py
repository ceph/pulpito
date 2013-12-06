from datetime import timedelta


def get_job_status_class(job):
    status = job['status'] or 'dead'
    if status == 'fail':
        status_class = 'danger'
    elif status == 'pass':
        status_class = 'success'
    else:
        status_class = 'warning'
    return status_class


def get_job_time_info(job):
    duration = job.get('duration')
    if duration:
        duration_pretty = str(timedelta(seconds=job['duration']))
        return duration_pretty
