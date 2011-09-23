#!/usr/bin/env python
import os.path
import json
import BaseHTTPServer
import webbrowser
import oauth.oauth as oauth
from urlparse import urlparse, parse_qs

import typepad
from typepad.tpclient import OAuthClient, TypePadClient

CONSUMER_KEY = 'bf50cd7ff782812d'
CONSUMER_SECRET = 'OIdo91f8'
APP_ID = '6p0154352e769b970c'

CONSUMER = None
OAUTH_CLIENT = None
TEMP_REQUEST_TOKEN = None
ACCESS_TOKEN = None

LOCAL_FILE = '.tp_access_token'
SERVER_NAME = '127.0.0.1'
SERVER_PORT = 8080
REDIRECT_URI = 'http://%s:%s/' % (SERVER_NAME, SERVER_PORT)

class _RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_GET(self):
        global ACCESS_TOKEN
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        params = parse_qs(urlparse(self.path).query)
        if 'oauth_verifier' in params:
            verifier = params.get('oauth_verifier', [None])[0]
            OAUTH_CLIENT.token = TEMP_REQUEST_TOKEN
            ACCESS_TOKEN = OAUTH_CLIENT.fetch_access_token(verifier=verifier)
            typepad.client.add_credentials(CONSUMER, ACCESS_TOKEN, domain="api.typepad.com")

        if ACCESS_TOKEN:
            data = {'access_token': {
                        'key': ACCESS_TOKEN.key,
                        'secret': ACCESS_TOKEN.secret,
                    }}
            open(LOCAL_FILE,'w').write(json.dumps(data))
            self.wfile.write("You have successfully logged in to typepad with tpconsole. "
                             "You can close this window now.")
        else:
            self.wfile.write('<html><head>'
                             '<script>location = "?"+location.hash.slice(1);</script>'
                             '</head></html>')

def authenticate():
    global ACCESS_TOKEN
    global TEMP_REQUEST_TOKEN
    global CONSUMER
    global OAUTH_CLIENT

    CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    app = typepad.Application.get_by_id(APP_ID)

    # Set up an oauth client for our signed requestses.
    OAUTH_CLIENT = OAuthClient(CONSUMER, None)
    OAUTH_CLIENT.request_token_url = app.oauth_request_token_url
    OAUTH_CLIENT.access_token_url = app.oauth_access_token_url
    OAUTH_CLIENT.authorization_url = app.oauth_authorization_url

    needs_auth = True
    if os.path.exists(LOCAL_FILE):
        data = json.loads(open(LOCAL_FILE).read())
        ACCESS_TOKEN = oauth.OAuthToken(data['access_token']['key'], data['access_token']['secret'])
        needs_auth = False
        typepad.client.add_credentials(CONSUMER, ACCESS_TOKEN, domain="api.typepad.com")

    if needs_auth:
        print "Logging you in to TypePad..."

        # Get a request token for the viewer to interactively authorize.
        TEMP_REQUEST_TOKEN = OAUTH_CLIENT.fetch_request_token(REDIRECT_URI)

        # Ask the viewer to authorize it.
        approve_url = OAUTH_CLIENT.authorize_token()
        webbrowser.open(approve_url)

        httpd = BaseHTTPServer.HTTPServer((SERVER_NAME, SERVER_PORT), _RequestHandler)
        while ACCESS_TOKEN is None:
            httpd.handle_request()

def _get_url(path):
    return 'https://api.typepad.com%s' % path

def me():
    c = TypePadClient()
    c.add_credentials(CONSUMER, ACCESS_TOKEN, domain="api.typepad.com")
    req = c.request(_get_url('/users/@self.json'))[1]
    return json.loads(req)

def tp(path, method="GET", body=None, headers=None):
    c = TypePadClient()
    c.add_credentials(CONSUMER, ACCESS_TOKEN, domain="api.typepad.com")
    req = c.request(_get_url(path), method=method, body=body, headers=headers)[1]
    return json.loads(req)

INTRO_MESSAGE = '''\
 _____  ____                            _
|_   _||  _ \                          | |
  | |  | |_) |___  ___  _ __  ___  ___ | | ___
  | |  |  _ // __|/ _ \| '_ \/ __|/ _ \| |/ _ \\
  | |  | |  | (__| (_) | | | \__ \ (_) | |  __/
  |_|  |_|   \___|\___/|_| |_|___/\___/|_|\___|

Type help() for a list of commands.
quick start:

  >>> authenticate()
  >>> print "Hello", me()['displayName']
  >>> print "My Blog URL: %s" % tp('/users/@self/blogs.json')['entries'][0]['homeUrl']

'''

def shell():
    try:
        from IPython.Shell import IPShellEmbed
        IPShellEmbed()(INTRO_MESSAGE)
    except ImportError:
        import code
        code.InteractiveConsole(globals()).interact(INTRO_MESSAGE)

if __name__ == '__main__':
    shell()
