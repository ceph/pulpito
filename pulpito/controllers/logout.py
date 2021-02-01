from pecan import expose, redirect
from pulpito.controllers import session

class LogoutController(object):

    def logout(self):
        cur_session = session.beaker_session()
        cur_session.delete()

    @expose('index.html')
    def index(self):
        self.logout()
        return redirect('/')