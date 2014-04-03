from collections import OrderedDict
from pecan import conf, expose, redirect
import requests

base_url = conf.paddles_address


class StatsController(object):

    @expose('node_stats.html')
    def nodes(self, machine_type=None, since_days=14):
        uri = '{base}/nodes/job_stats?since_days={days}'.format(
            base=base_url,
            days=since_days)
        if machine_type:
            uri += '&machine_type=%s' % machine_type

        response = requests.get(uri, timeout=60)
        if response.status_code == 502:
            redirect('/errors?status_code={status}&message={msg}'.format(
                status=200, msg='502 gateway error :('),
                internal=True)

        nodes = response.json()
        statuses = ['pass', 'fail', 'dead', 'unknown', 'running']
        for name in nodes.keys():
            node = nodes[name]
            total = sum(node.values())
            node['total'] = total
            for status in statuses:
                if node.get(status) is None:
                    node[status] = 0
        nodes = OrderedDict(
            sorted(nodes.items(), key=lambda t: t[1]['total'], reverse=True))
        return dict(
            machine_type=machine_type,
            days=since_days,
            nodes=nodes,
            count=len(nodes),
        )
