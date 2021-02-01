from pecan import conf, make_app, request
from pulpito import model
from pulpito.filters import setup_filters
from beaker.middleware import SessionMiddleware


def setup_app(config):

    setup_filters()
    model.init_model()
    app_conf = dict(config.app)
    app = make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        **app_conf
    )
    app = SessionMiddleware(app, conf.beaker)
    return app
