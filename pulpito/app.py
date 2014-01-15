from pecan import conf, make_app
from pulpito import model
from pulpito.filters import setup_filters


def setup_app(config):

    setup_filters()
    model.init_model()
    app_conf = dict(config.app)

    return make_app(
        app_conf.pop('root'),
        logging=getattr(config, 'logging', {}),
        extra_template_vars=dict(paddles_address=conf.paddles_address),
        **app_conf
    )
