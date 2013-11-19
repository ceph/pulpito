from pecan import conf, expose
import requests

from job import JobController
from util import get_job_status_info, get_job_time_info
from pulpito.controllers import error
from pulpito.controllers.errors import ErrorsController

base_url = conf.paddles_address


class RootController(object):

    errors = ErrorsController()

    @expose('index.html')
    def index(self):
        latest_runs = requests.get('{base}/runs/'.format(base=base_url)).json()
        for run in latest_runs:
            run['status_class'] = self.set_status_class(run)
        return dict(runs=latest_runs)

    def set_status_class(self, run):
        fail = run['results']['fail']
        running = run['results']['running']
        passing = run['results']['pass']
        status_class = 'warning'
        if fail:
            status_class = 'danger'
        elif not running and passing:
            status_class = 'success'
        elif running and passing:
            status_class = 'warning'
        else:
            status_class = 'warning'
        return status_class

    @expose('index.html')
    def date(self, from_date_str, to=None, to_date_str=None):
        if to:
            resp = requests.get(
                '{base}/runs/date/from/{from_}/to/{to}'.format(
                    base=base_url, from_=from_date_str, to=to_date_str))
        else:
            resp = requests.get('{base}/runs/date/{date}/'.format(
                base=base_url, date=from_date_str))

        if resp.status_code == 400:
            error('/errors/invalid/',
                  resp.json().get('message'))
        elif resp.status_code == 404:
            error('/errors/not_found/',
                  resp.json().get('message'))
        else:
            runs = resp.json()

        for run in runs:
            run['status_class'] = self.set_status_class(run)
        return dict(runs=runs)

    @expose('compare.html')
    def compare(self, suite, branch, count=3):
        """
        Ask paddles for a list of runs of ``suite`` on ``branch``, then build a
        dict that looks like:
            {'runs': [
                {'name': run_name,
                    'jobs': [
                        job_description: {
                            'job_id': job_id,
                            'success': success }
                    ]}
                ]
             'descriptions': [
                 job_description,
                ]
            }
        """
        runs = requests.get(
            '{base}/runs/branch/{branch}/suite/{suite}/?count={count}'.format(
                base=base_url,
                branch=branch,
                suite=suite,
                count=str(count))).json()
        full_info = dict(
            branch=branch,
            suite=suite,
            runs=list(),
        )
        descriptions = set()
        for run in runs:
            run_info = dict()
            resp = requests.get(
                '{base}/runs/{run_name}/jobs/?fields=job_id,description,success,log_href,failure_reason'.format(  # noqa
                    base=base_url,
                    run_name=run['name']))

            if resp.status_code == 404:
                error('/errors/not_found/')
            else:
                jobs = resp.json()

            run_info['name'] = run['name']
            run_info['scheduled'] = run['scheduled']
            run_info['jobs'] = dict()
            for job in jobs:
                description = job.pop('description')
                job['status'], job['status_class'] = get_job_status_info(job)
                job['duration_pretty'] = get_job_time_info(job)
                descriptions.add(description)
                run_info['jobs'][description] = job
            full_info['runs'].append(run_info)
        full_info['runs'].reverse()
        full_info['descriptions'] = sorted(list(descriptions))
        return full_info

    @expose()
    def _lookup(self, name, *remainder):
        return RunController(name), remainder


class RunController(object):

    def __init__(self, name):
        self.name = name
        self.run = None

    def get_run(self):
        resp = requests.get(
            '{base}/runs/{name}'.format(base=base_url,
                                        name=self.name))
        if resp.status_code == 404:
            error('/errors/not_found/',
                  'requested run does not exist')
        else:
            run = resp.json()

        if 'scheduled' in run:
            run['scheduled_day'] = run['scheduled'].split()[0]

        if 'jobs' in run:
            for job in run['jobs']:
                job['status'], job['status_class'] = get_job_status_info(job)
                job['duration_pretty'] = get_job_time_info(job)

        self.run = run
        return self.run

    @expose('run.html')
    def index(self):
        run = self.run or self.get_run()
        return dict(
            run=run
        )

    @expose('json')
    def _lookup(self, job_id, *remainder):
        return JobController(self.name, job_id), remainder
