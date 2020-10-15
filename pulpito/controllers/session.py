from pecan import request
from beaker.middleware import SessionMiddleware

def beaker_session():
        return request.environ.get("beaker.session")