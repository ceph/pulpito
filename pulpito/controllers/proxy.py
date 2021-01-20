from pecan import conf, expose
import requests
from urllib.parse import urljoin


class ProxyController(object):
    """
    Allows the client to indirectly query a paddles instance. Useful if paddles
    lives behind a firewall, but pulpito does not.
    """
    base_url = conf.paddles_address

    def __init__(self, query):
        self.query = query

    @expose('json')
    def branches(self):
        url = urljoin(self.base_url, '/runs/branch/')
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

    @expose('json')
    def machine_types(self):
        url = urljoin(self.base_url, '/nodes/machine_types/')
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()

    @expose('json')
    def suites(self):
        url = urljoin(self.base_url, '/runs/suite/')
        resp = requests.get(url)
        resp.raise_for_status()
        return resp.json()
