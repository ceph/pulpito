from pecan import expose
import requests


class RootController(object):

    @expose('index.html')
    def index(self):
        latest_runs = requests.get('http://sentry.front.sepia.ceph.com:8080/runs/').json()['latest_runs']
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

    @expose()
    def _lookup(self, name, *remainder):
        return RunController(name), remainder


class RunController(object):

    def __init__(self, name):
        self.name = name

    @expose('run.html')
    def index(self):
        metadata = requests.get('http://sentry.front.sepia.ceph.com:8080/runs/%s' % self.name).json()
        for job in metadata['jobs']:
            job['status_class'] = self.set_status_class(job)
        return dict(
            run=metadata
        )

    def set_status_class(self, job):
        success = job['success']
        if success is False:
            status_class = 'danger'
        elif success:
            status_class = 'success'
        elif success is None:
            status_class = 'warning'
        else:
            status_class = 'warning'
        return status_class
