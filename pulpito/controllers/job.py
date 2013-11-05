from pecan import expose
from pecan import conf
import requests
from util import get_job_status_info

base_url = conf.paddles_address


class JobController(object):
    def __init__(self, run_name, job_id):
        self.run_name = run_name
        self.job_id = job_id
        self.job = requests.get("{base}/runs/{run}/jobs/{job}".format(
            base=base_url, run=run_name, job=job_id)).json()
        status_info = get_job_status_info(self.job)
        self.job['status'], self.job['status_class'] = status_info

    @expose('job.html')
    def index(self):
        return dict(job=self.job)
