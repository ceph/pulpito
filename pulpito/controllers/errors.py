from pecan import expose, response


class ErrorsController(object):

    @expose('error.html')
    def invalid(self, **kw):
        msg = kw.get(
            'error_message',
            'invalid request'
        )
        response.status = 400
        return dict(status=response.status, message=msg)

    @expose('error.html')
    def not_found(self, **kw):
        msg = kw.get(
            'error_message',
            'resource was not found'
        )
        status = 404
        return dict(status=status, message=msg)