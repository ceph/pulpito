from pecan import expose
from pecan import conf
import requests
import urlparse
from util import prettify_job
from pulpito.controllers import error

base_url = conf.paddles_address


class JobController(object):
    def __init__(self, run_name, job_id):
        self.run_name = run_name
        self.job_id = job_id
        url = urlparse.urljoin(
            base_url,
            "/runs/{0}/jobs/{1}/".format(run_name, job_id)
        )
        resp = requests.get(url)
        if resp.status_code == 400:
            error('/errors/invalid/')
        elif resp.status_code == 404:
            error('/errors/not_found/')
        else:
            self.job = resp.json()
            prettify_job(self.job)

    @expose('job.html')
    def index(self):
        return dict(job=self.job)
