from pecan import conf, expose, redirect, request, abort
from requests_oauthlib import OAuth2Session
import urlparse
import os
import json
from dotenv import load_dotenv, find_dotenv
from pulpito.controllers import session


# TODO: Uncomment for development without https
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

load_dotenv(find_dotenv())

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET= os.getenv("CLIENT_SECRET")
AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"

github = OAuth2Session(CLIENT_ID)

class CallbackController(object):


    def user_is_in_ceph_org(self):
        token = github.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET,
                               authorization_response=request.url)
        user_details = github.get('https://api.github.com/user').json()
        username = user_details["login"]
        user_org_url = user_details["organizations_url"]
        user_org_list = github.get(user_org_url).json()
        for org in user_org_list:
            if org["login"] == "ceph":
                cur_session = session.beaker_session()
                cur_session["username"] = username
                cur_session.save()
                return True
        return False

    @expose('index.html')
    def index(self):
        if self.user_is_in_ceph_org():
            return redirect('/')
        else:
            return abort(401)

class LoginController(object):

    def login(self):
        authorization_url, state = github.authorization_url(AUTHORIZATION_BASE_URL)
        return redirect(authorization_url)


    @expose()
    def index(self):
        self.login()
        return redirect('/')


    callback = CallbackController()



