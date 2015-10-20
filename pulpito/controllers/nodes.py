from pecan import conf, expose, redirect
from pulpito.controllers import error
from pulpito.controllers.util import set_node_status_class, prettify_job
import requests

base_url = conf.paddles_address


class NodesController(object):
    @expose('nodes.html')
    def index(self, machine_type=None):
        uri = '{base}/nodes/'.format(
            base=base_url,
        )
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
        return dict(
            title=title,
            nodes=nodes,
        )

    @expose()
    def _lookup(self, name, *remainder):
        return NodeController(name), remainder


class NodeController(object):
    def __init__(self, name):
        self.name = name
        self.node = None

    def get_node(self):
        resp = requests.get(
            '{base}/nodes/{name}'.format(base=base_url,
                                         name=self.name))
        if resp.status_code == 404:
            error('/errors/not_found/',
                  'requested node does not exist')
        else:
            node = resp.json()

        set_node_status_class(node)
        self.node = node
        self.get_node_jobs()
        return self.node

    def get_node_jobs(self, count=5):
        resp = requests.get(
            '{base}/nodes/{name}/jobs/?count={count}'.format(
                base=base_url,
                name=self.name,
                count=count,
            )
        )

        jobs = resp.json()
        for job in jobs:
            prettify_job(job)
        self.node['jobs'] = jobs
        return self.node

    @expose('nodes.html')
    def index(self):
        node = self.node or self.get_node()
        return dict(
            nodes=[node]
        )
