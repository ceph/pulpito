from os import path
from pecan import request, redirect


def error(url, msg=None):
    if msg:
        request.context['error_message'] = msg
    url = path.join(url, '?error_message=%s' % msg)
    redirect(url, internal=True)
