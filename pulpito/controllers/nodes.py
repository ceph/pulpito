from pecan import conf, expose, redirect
from pulpito.controllers import error
from pulpito.controllers.util import set_node_status_class
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
        nodes.sort(key=lambda n: n['name'])

        title = "{mtype} nodes".format(
            mtype=machine_type if machine_type else 'All',
        )
        return dict(
            title=title,
            nodes=nodes,
        )
