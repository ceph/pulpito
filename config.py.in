# Server Specific Configurations
server = {
    'port': '8080',
    'host': '0.0.0.0'
}

paddles_address = 'http://sentry.front.sepia.ceph.com:8080'

# Pecan Application Configurations
app = {
    'root': 'pulpito.controllers.root.RootController',
    'modules': ['pulpito'],
    'static_root': '%(confdir)s/public',
    'template_path': '%(confdir)s/pulpito/templates',
    'default_renderer': 'jinja',
    'debug': True,
    'errors': {
        404: '/error/404',
        '__force_dict__': True
    }
}

logging = {
    'loggers': {
        'root': {'level': 'INFO', 'handlers': ['console']},
        'pulpito': {'level': 'DEBUG', 'handlers': ['console']},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        }
    }
}

# Custom Configurations must be in Python dictionary format::
#
# foo = {'bar':'baz'}
#
# All configurations are accessible at::
# pecan.conf
