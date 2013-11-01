from pecan import expose
from pecan import conf
import requests

base_url = conf.paddles_address


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
        status = '?'
    return status, status_class


class RootController(object):

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
            jobs = requests.get(
                '{base}/runs/{run_name}/jobs/?fields=job_id,description,success'.format(  # noqa
                    base=base_url,
                    run_name=run['name'])).json()
            run_info['name'] = run['name']
            run_info['jobs'] = dict()
            for job in jobs:
                description = job.pop('description')
                job['status'], job['status_class'] = get_job_status_info(job)
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

    @expose('run.html')
    def index(self):
        metadata = requests.get(
            '{base}/runs/{name}'.format(base=base_url,
                                        name=self.name)).json()
        for job in metadata['jobs']:
            job['status_class'] = get_job_status_info(job)[1]
        return dict(
            run=metadata
        )
