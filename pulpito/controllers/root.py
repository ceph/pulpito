from pecan import conf, expose, request
import requests
from urllib.parse import urljoin, urlencode


from pulpito.controllers import error, session
from pulpito.controllers.compare import RunCompareController
from pulpito.controllers.errors import ErrorsController
from pulpito.controllers.job import JobController
from pulpito.controllers.nodes import NodesController
from pulpito.controllers.proxy import ProxyController
from pulpito.controllers.queue import QueueController
from pulpito.controllers.stats import StatsController
from pulpito.controllers.util import get_run_filters, prettify_run, prettify_job
from pulpito.controllers.login import LoginController
from pulpito.controllers.logout import LogoutController

base_url = conf.paddles_address

run_sorter = lambda run: run['scheduled']


class RootController(object):

    errors = ErrorsController()
    @expose('index.html')
    def index(self, latest=False, branch='', machine_type='', sha1='',
              status='', suite='', date='', to_date='', page='1'):
        filters = get_run_filters(
            latest=latest, branch=branch, machine_type=machine_type, sha1=sha1,
            status=status, suite=suite, date=date, to_date=to_date,
        )
        request.context['filters'] = filters
        urlencode_args = dict()

        uri = urljoin(base_url, '/runs/')
        if branch:
            uri += 'branch/%s/' % branch
        if machine_type:
            uri += 'machine_type/%s/' % machine_type
        if sha1:
            uri += 'sha1/%s/' % sha1
        if status:
            uri += 'status/%s/' % status
        if suite:
            uri += 'suite/%s/' % suite
        if to_date and date:
            uri += 'date/from/{from_}/to/{to}/'.format(from_=date, to=to_date)
        elif date:
            uri += 'date/%s/' % date
        if status == 'running':
            urlencode_args['count'] = 9999
        if int(page) > 1:
            urlencode_args['page'] = page
        if urlencode_args:
            uri += '?%s' % urlencode(urlencode_args)

        latest_runs = requests.get(uri).json()
        for run in latest_runs:
            prettify_run(run)
        latest_runs.sort(key=run_sorter, reverse=True)
        cur_session = session.beaker_session()
        return dict(runs=latest_runs,
                    filters=request.context.get('filters', dict()),
                    branch=branch,
                    machine_type=machine_type,
                    suite=suite,
                    dates=[date, to_date],
                    page=page,
                    sha1=sha1,
                    session=cur_session
                    )

    @expose('index.html')
    def latest(self, **kwargs):
        return self.index(latest=True, **kwargs)

    @expose('index.html')
    def date(self, from_date_str, to='', to_date_str=''):
        filters = get_run_filters(date=from_date_str, to_date=to_date_str)
        request.context['filters'] = filters
        if to:
            url = urljoin(
                base_url,
                '/runs/date/from/{0}/to/{1}'.format(
                    from_date_str, to_date_str)
            )
        else:
            url = urljoin(
                base_url,
                '/runs/date/{0}/'.format(from_date_str)
            )
        resp = requests.get(url)

        if resp.status_code == 400:
            error('/errors/invalid/',
                  resp.json().get('message'))
        elif resp.status_code == 404:
            error('/errors/not_found/',
                  resp.json().get('message'))
        else:
            runs = resp.json()

        for run in runs:
            prettify_run(run)
        runs.sort(key=run_sorter)
        cur_session = session.beaker_session()
        return dict(runs=runs,
                    filters=request.context.get('filters', dict()),
                    dates=[from_date_str, to_date_str],
                    session=cur_session
                    )

    compare = RunCompareController()

    nodes = NodesController()

    stats = StatsController()

    queue = QueueController()

    login = LoginController()
    
    logout = LogoutController()

    @expose()
    def _lookup(self, name, *remainder):
        if name == '_paddles':
            return ProxyController(query=name), remainder
        return RunController(name), remainder


class RunController(object):

    def __init__(self, name):
        self.name = name
        self.run = None

    def get_run(self):
        url = urljoin(base_url, '/runs/%s/' % self.name)
        resp = requests.get(url)
        if resp.status_code == 404:
            error('/errors/not_found/',
                  'requested run does not exist')
        else:
            run = resp.json()

        if 'scheduled' in run:
            run['scheduled_day'] = run['scheduled'].split()[0]

        if 'jobs' in run:
            for job in run['jobs']:
                prettify_job(job)

        prettify_run(run)
        self.run = run
        return self.run

    @expose('run.html')
    def index(self):
        run = self.run or self.get_run()
        cur_session = session.beaker_session()
        return dict(
            run=run,
            session=cur_session
        )

    @expose('run_detail.html')
    def detail(self):
        run = self.run or self.get_run()
        cur_session = session.beaker_session()
        return dict(
            run=run,
            session=cur_session
        )

    @expose('json')
    def _lookup(self, job_id, *remainder):
        return JobController(self.name, job_id), remainder
