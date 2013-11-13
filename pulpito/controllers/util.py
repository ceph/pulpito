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
        status = 'running?'
    return status, status_class
