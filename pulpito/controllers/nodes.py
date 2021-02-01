from pecan import conf, expose, redirect
from pulpito.controllers import error, session
from pulpito.controllers.util import set_node_status_class, prettify_job
from urllib.parse import urljoin
import requests

base_url = conf.paddles_address


class NodesController(object):
    @expose('nodes.html')
    def index(self, machine_type=None):
        uri = urljoin(base_url, '/nodes/')
        if machine_type:
            uri += '?machine_type=%s' % machine_type

        resp = requests.get(uri, timeout=60)
        if resp.status_code == 502:
            redirect('/errors?status_code={status}&message={msg}'.format(
                status=200, msg='502 gateway error :('),
                internal=True)
        elif resp.status_code == 400:
            error('/errors/invalid/', msg=resp.text)

        nodes = resp.json()
        for node in nodes:
            set_node_status_class(node)
            # keep only the node name, not the fqdn
            node['fqdn'] = node['name']
            node['name'] = node['fqdn'].split(".")[0]
            desc = node['description']
            if not desc or desc.lower() == "none":
                node['description'] = ""
            elif 'teuthworker' in desc:
                # strip out the path part of the description and
                # leave it with the run_name/job_id
                node['description'] = "/".join(desc.split("/")[-2:])
        nodes.sort(key=lambda n: n['name'])

        title = "{mtype} nodes".format(
            mtype=machine_type if machine_type else 'All',
        )
        cur_session = session.beaker_session()
        return dict(
            title=title,
            nodes=nodes,
            session=cur_session
        )

    @expose()
    def _lookup(self, name, *remainder):
        return NodeController(name), remainder


class NodeController(object):
    def __init__(self, name):
        self.name = name
        self.node = None

    def get_node(self, page=None):
        url = urljoin(base_url, '/nodes/{0}/'.format(self.name))
        resp = requests.get(url)
        if resp.status_code == 404:
            error('/errors/not_found/',
                  'requested node does not exist')
        else:
            node = resp.json()

        set_node_status_class(node)
        self.node = node
        self.get_node_jobs(page=page)
        return self.node

    def get_node_jobs(self, count=20, page=None):
        page = page or 1
        url = urljoin(
            base_url,
            '/nodes/{0}/jobs/?count={1}&page={2}'.format(
                self.name, count, page)
        )
        resp = requests.get(url)

        jobs = resp.json()
        for job in jobs:
            prettify_job(job)
        self.node['jobs'] = jobs
        return self.node

    @expose('nodes.html')
    def index(self, page=1):
        node = self.node or self.get_node(page=page)
        cur_session = session.beaker_session()
        return dict(
            nodes=[node],
            page=page,
            session=cur_session
        )
