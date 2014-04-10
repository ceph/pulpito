from pulpito.controllers import util


class TestUtil(object):
    def test_run_status_class(self):
        run = {'status': 'pass'}
        util.set_run_status_class(run)
        assert run['status_class'] == 'success'

    def test_run_scheduled(self):
        run = {'scheduled': '2014-03-18 21:29:46.351053'}
        util.set_run_time_info(run)
        assert run['scheduled'] == '2014-03-18 21:29:46'

    def test_run_started(self):
        run = {'started': '2014-03-18 21:29:46.351053', 'status': 'running'}
        util.set_run_time_info(run)
        assert 'runtime' in run
