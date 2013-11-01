from pecan import expose
from pecan import conf
import requests

base_url = conf.paddles_address


class JobController(object):
    def __init__(self, run_name, job_id):
        self.run_name = run_name
        self.job_id = job_id
        self.job = requests.get("{base}/runs/{run}/jobs/{job}".format(
            base=base_url, run=run_name, job=job_id)).json()

    @expose('json')
    def index(self):
        return self.job
