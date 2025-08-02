import os
import cherrypy
from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

from pecan.deploy import deploy
from urllib.parse import unquote

import prod

prod_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'prod.py'))
simpleapp_wsgi_app = deploy(prod_config)

public_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'public'))

# A dummy class for our Root object
# necessary for some CherryPy machinery
class Root(object):
    pass

def teuthology_app(environ, start_response):
    path = unquote(environ.get('PATH_INFO', '')).strip('/')
    if not path.startswith('teuthology/'):
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Invalid request']

    segments = path.split('/')
    if len(segments) < 4:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Invalid path structure']

    _, run, job_id, filename = segments[:4]
    archive_root = os.environ.get('PULPITO_ARCHIVE', '')
    log_path = os.path.join(archive_root, run, job_id, filename)

    if not os.path.exists(log_path):
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return [b'Log not found']

    try:
        with open(log_path, 'rb') as f:
            content = f.read()
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [f"----------LOG START----------".encode() + content]
    except Exception as e:
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [f'Error reading file: {e}'.encode()]


def make_static_config(static_dir_name):
    """
    All custom static configurations are set here, since most are common, it
    makes sense to generate them just once.
    """
    static_path = os.path.join('/', static_dir_name)
    path = os.path.join(public_path, static_dir_name)
    configuration = {
        static_path: {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': path
        }
    }
    return cherrypy.tree.mount(Root(), '/', config=configuration)

# Assuming your app has media on diferent paths, like 'css', and 'images'
application = PathInfoDispatcher({
    '/': simpleapp_wsgi_app,
    '/css': make_static_config('css'),
    '/js': make_static_config('js'),
    '/images': make_static_config('images'),
    '/fonts': make_static_config('fonts'),
    '/favicon.ico': make_static_config('images'),
    '/teuthology': teuthology_app,
})

def final_app(environ, start_response):
    if environ.get('PATH_INFO', '').startswith('/teuthology/'):
        return teuthology_app(environ, start_response)
    return application(environ, start_response)

server = WSGIServer(
    (prod.server['host'], int(prod.server['port'])),
    final_app
)

try:
    server.start()
except KeyboardInterrupt:
    print("Terminating server...")
    server.stop()