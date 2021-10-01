from pecan import conf, expose
import requests
from urllib.parse import urljoin

from pulpito.controllers import error
from pulpito.controllers.util import prettify_job

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
                            'status': status }
                    ]}
                ]
             'descriptions': [
                 job_description,
                ]
            }
        """
        url = urljoin(
            base_url,
            '/runs/branch/{branch}/suite/{suite}/?count={count}'.format(
                branch=branch,
                suite=suite,
                count=str(count))
        )
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
            url = urlparse.urljoin(
                base_url,
                '/runs/{0}/jobs/?fields=job_id,description,status,log_href,failure_reason'.format(  # noqa
                    run['name'])
            )
            resp = requests.get(url)

            if resp.status_code == 404:
                error('/errors/not_found/')
            else:
                jobs = resp.json()

            run_info['name'] = run['name']
            run_info['scheduled'] = run['scheduled']
            run_info['jobs'] = dict()
            for job in jobs:
                description = job.pop('description')
                prettify_job(job)
                descriptions.add(description)
                run_info['jobs'][description] = job
            full_info['runs'].append(run_info)
        full_info['runs'].reverse()
        full_info['descriptions'] = sorted(list(descriptions))
        return full_info
