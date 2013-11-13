from datetime import timedelta


def get_job_status_info(job):
    success = job['success']
    if success is False:
        status_class = 'danger'
        status = 'fail'
    elif success is True:
        status_class = 'success'
        status = 'pass'
    else:
        status_class = 'warning'
        status = 'running'
    return status, status_class


def get_job_time_info(job):
    duration = job.get('duration')
    if duration:
        duration_pretty = str(timedelta(seconds=job['duration']))
        return duration_pretty
