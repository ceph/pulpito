from pecan import conf, expose
import requests

from util import prettify_run

base_url = conf.paddles_address


class QueueController(object):
    @expose('index.html')
    def index(self):
        url = "{base}/runs/queued/".format(base=base_url)
        resp = requests.get(url)
        runs = resp.json()
        for run in runs:
            prettify_run(run)
        return dict(
            title="The Queue",
            runs=runs,
        )


