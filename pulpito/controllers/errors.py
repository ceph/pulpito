from pecan import expose, response
from pulpito.controllers import session

class ErrorsController(object):
    
    @expose('error.html')
    def index(self, status_code, message):
        response.status = status_code
        cur_session = session.beaker_session()
        return dict(status=status_code, message=message, session=cur_session)

    @expose('error.html')
    def invalid(self, **kw):
        msg = kw.get(
            'error_message',
            'invalid request'
        )
        response.status = 400
        cur_session = session.beaker_session()
        return dict(status=response.status, message=msg, session=cur_session)

    @expose('error.html')
    def not_found(self, **kw):
        msg = kw.get(
            'error_message',
            'resource was not found'
        )
        response.status = 404
        cur_session = session.beaker_session()
        return dict(status=response.status, message=msg, session=cur_session)
