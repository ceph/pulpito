from pecan import expose
import requests


class RootController(object):

    @expose('index.html')
    def index(self):
        latest_runs = requests.get('http://sentry.front.sepia.ceph.com:8080/runs/').json()['latest_runs']
        runs = {}
        for run in latest_runs:
            runs[run['name']] = self.get_run_metadata(run['name'])
        return dict(runs=self.set_status_class(runs))

    def get_run_metadata(self, run_name):
        metadata = requests.get('http://sentry.front.sepia.ceph.com:8080/runs/%s' % run_name).json()
        return metadata

    def set_status_class(self, runs):
        for run in runs:
            run = runs[run]
            fail = run['results']['fail']
            running = run['results']['running']
            passing = run['results']['pass']

            if fail:
                run['status_class'] = 'danger'
            elif not running and passing:
                run['status_class'] = 'success'
            elif running and passing:
                run['status_class'] = 'warning'
            else:
                run['status_class'] = 'warning'
        return runs
