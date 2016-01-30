from __future__ import print_function

'''
Methods Related to processing approvals.
All of these will require validation
'''
__all__ = (
    "SubmissionApprove",
    "SubmissionReject",
    "AdminRideCancel",
)

import httplib2
import os
import jinja2
import webapp2
from webapp2_extras import sessions

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

from apiclient import discovery

import oauth2client
from oauth2client import client
from oauth2client import tools
from oauth2client.appengine import StorageByKeyName
from oauth2client.appengine import CredentialsNDBModel

import datetime



SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'credentials/client_secret.json'
APPLICATION_NAME = 'Ridelister'

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# http://stackoverflow.com/questions/15493062/store-access-token-from-google-oauth-2-0-to-access-drive-data-from-application-a

def get_credentials(user_id):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    storage = StorageByKeyName(CredentialsNDBModel, user_id, 'credentials')
    credentials = storage.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(
               CLIENT_SECRET_FILE,
               SCOPES,
               redirect_uri="https://localhost:8080/oauth2callback",
               )

        # Todo - Look this one up...
        flow.user_agent = APPLICATION_NAME
        # credentials = tools.run_flow(flow, storage)
        # print('Storing credentials')
        auth_uri = flow.step1_get_authorize_url()
    return credentials

# Here's the thing that handles the URL hit from the 
# Google authentication system.
class SubmissionGoogleAuth(webapp2.RequestHandler):
    def get(self):

        get_values = request.GET
        
        # This approximately follows the flow provided by google.
        # if we land here, we cat get real credentials.
        if 'code' in get_values.keys()
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE,SCOPES
                redirect_uri="https://localhost:8080/oauth2callback" )
            credentials = flow.step2_exchange(get_values{'code'})
            # Stuff them into the session area.
            self.session['credentials'] = credentials.to_json()
            self.redirect('/approve')
        else:
            auth_uri = flow.step1_get_authorize_url()
            self.redirect(auth_uri)
        return


class SubmissionApprove(webapp2.RequestHandler):
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session(backend='memcache')
        # return self.session_store.get_session()
        
    def get(self):

        # We'll use the nickname as a credentials key.
        user = users.get_current_user()
    
        if user:
            greeting = 'Ride Submission by ' + user.nickname()
        else:
            greeting = 'You must be logged in to get a confirmation email'
            self.redirect(users.create_login_url(self.request.uri))

        # Get Credentials
        credentials = get_credentials(user.nickname())
        # http = credentials.authorize(httplib2.Http())
        # service = discovery.build('calendar', 'v3', http=http)
    
        # Save something in the session
        self.session['foo'] = 'bar'

        if user:
            nick = user.nickname()
        else:
            self.redirect(users.create_login_url(self.request.uri))
       
        textkey = self.request.get('dbkey')

        # There should be some error checking here.

        entrykey = ndb.Key(urlsafe=textkey)        
        ridelisting = entrykey.get()

        template_values = {
            'approvernickname': nick,
            'ridename': ridelisting.name,
            'ridestartlocation': ridelisting.startlocation,
            'ridestartdate': ridelisting.startdate,
            'ridedescription': ridelisting.description,
            'creation': ridelisting.created,
            'modified': ridelisting.modified,
            'ridedbkey': textkey,
            'sessioninfo': self.session.get('foo'),
            }

        # Go ahead and render it out for the user
        template = JINJA_ENVIRONMENT.get_template('submissionapprove.html')
        self.response.write(template.render(template_values))
    

class SubmissionReject(webapp2.RequestHandler):
    def get(self):

        # Get Credentials
        user = users.get_current_user()

        if user:
            greeting = 'Hello, ' + user.nickname()
        else:
            self.redirect(users.create_login_url(self.request.uri))

        template_values = {
            'greeting': greeting,
            }

        template = JINJA_ENVIRONMENT.get_template('submissionreject.html')
        self.response.write(template.render(template_values))

class AdminRideCancel(webapp2.RequestHandler):
    def get(self):

        # Get Credentials
        user = users.get_current_user()

        if user:
            greeting = 'Hello, ' + user.nickname()
        else:
            self.redirect(users.create_login_url(self.request.uri))

        template_values = {
            'greeting': greeting,
            }

        template = JINJA_ENVIRONMENT.get_template('ridecancellation.html')
        self.response.write(template.render(template_values))

