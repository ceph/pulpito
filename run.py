import os
import cherrypy
from cheroot.wsgi import Server as WSGIServer, PathInfoDispatcher

from pecan.deploy import deploy

import prod

prod_config = os.path.abspath(os.path.join(os.path.dirname(__file__), 'prod.py'))
simpleapp_wsgi_app = deploy(prod_config)

public_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'public'))

# A dummy class for our Root object
# necessary for some CherryPy machinery
class Root(object):
    pass

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
})

server = WSGIServer(
    (prod.server['host'], int(prod.server['port'])),
    application
)

try:
    server.start()
except KeyboardInterrupt:
    print("Terminating server...")
    server.stop()