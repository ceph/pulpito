from pecan import expose
from pecan import conf
import requests
from urllib.parse import urljoin
from pulpito.controllers import error, session
from pulpito.controllers.util import prettify_job

base_url = conf.paddles_address


class JobController(object):
    def __init__(self, run_name, job_id):
        self.run_name = run_name
        self.job_id = job_id
        url = urljoin(
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
        cur_session = session.beaker_session()
        return dict(job=self.job, session=cur_session)
