from util import get_job_status_info, get_job_time_info
from pecan import conf, expose
import requests

from pulpito.controllers import error

base_url = conf.paddles_address


class RunCompareController(object):
    @expose('compare.html')
    def index(self, suite, branch, since=None, count=3):
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
        url = '{base}/runs/branch/{branch}/suite/{suite}/?count={count}'.format(  # noqa
            base=base_url,
            branch=branch,
            suite=suite,
            count=str(count))
        if since:
            url += '&since=' + since

        runs = requests.get(url).json()
        full_info = dict(
            branch=branch,
            suite=suite,
            since=since,
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
