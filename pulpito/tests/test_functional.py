from pulpito.tests import FunctionalTest


class TestRootController(FunctionalTest):

    def test_get(self):
        response = self.app.get('/')
        assert response.status_int == 200

    def test_run_not_found(self):
        response = self.app.get('/not_a_run/', expect_errors=True)
        assert response.status_int == 404

    def test_job_not_found(self):
        response = self.app.get('/not_a_run/or_job/', expect_errors=True)
        assert response.status_int == 404

    def test_other_not_found(self):
        response = self.app.get('/not_a_run/or_job/or_anything_else/',
                                expect_errors=True)
        assert response.status_int == 404
