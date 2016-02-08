from __future__ import print_function

'''
Methods Related to processing approvals.
All of these will require validation
'''
__all__ = (
    "SubmissionGoogleAuth",
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

from ridelib.config import *


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
               redirect_uri=ridelisterconfig['ridelister']['callbackurl'],
               # redirect_uri="https://localhost:8080/oauth2callback",
               )

        # Todo - Look this one up...
        flow.user_agent = APPLICATION_NAME
        # credentials = tools.run_flow(flow, storage)
        # print('Storing credentials')
        auth_uri = str(flow.step1_get_authorize_url())
    
    return credentials

##################################################################################
##################################################################################
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
        if 'credentials' not in self.session:
            self.redirect('http://ridelister-1191.appspot.com/oauth2callback')
            return

        credentials = client.OAuth2Credentials.from_json(self.session.get('credentials'))
        if credentials.access_token_expired:
            self.redirect('http://ridelister-1191.appspot.com/oauth2callback')
            return

        http = credentials.authorize(httplib2.Http())
        service = discovery.build('calendar', 'v3', http=http)
        

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        print('Getting the upcoming 10 events')
        eventsResult = service.events().list(
            calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])

        formatted = 'Data: '
        
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            formatted.join(start + event['summary'])

        # We'll use the nickname as a credentials key.
        user = users.get_current_user()

        if user:
            greeting = 'Ride Submission by ' + user.nickname()

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
            'sessioninfo': now,
            'payload' : formatted
            }

        # Go ahead and render it out for the user
        template = JINJA_ENVIRONMENT.get_template('submissionapprove.html')
        self.response.write(template.render(template_values))


        # Now that we've sent the form response, send the confirmation email.
        # There should have been a checkbox in case they didn't want it.

        message = mail.EmailMessage(sender="Ride Lister <robert@kudra.com>",
                                    subject="Your ride listing has been published")

        message.body = """

Thanks for submitting your ride!

It has been approved and is now visible on the club calendar

<p>Ride Name: %s
<p>Ride Starting Location: %s
<p>Ride Description: %s


<p>If you need to cancel this ride, please do so here: <a href="cancel?dbkey=%s">Edit</a>
<p>If you would like to re-use this ride listing, go here: <a href="resubmit?dbkey=%s">Edit</a>

        """ % (
            ridelisting.name,
            ridelisting.startlocation,
            ridelisting.description,
            textkey,textkey)

        if user:
            message.to = user.email()
            message.send()



##################################################################################
# Here's the thing that handles the URL hit from the 
# Google authentication system.
##################################################################################
class SubmissionGoogleAuth(webapp2.RequestHandler):
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
 
    def get(self):
        get_values = self.request.GET

        # This approximately follows the flow provided by google.
        # if we land here, we cat get real credentials.
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE,SCOPES,
               redirect_uri='http://ridelister-1191.appspot.com/oauth2callback' )
        if 'code' in get_values:
            credentials = flow.step2_exchange(get_values['code'])
            # Stuff them into the session area.
            self.session['credentials'] = credentials.to_json()
            self.redirect('/approve')
        else:
            auth_uri = str(flow.step1_get_authorize_url())
            self.redirect(auth_uri)


##################################################################################
##################################################################################
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

##################################################################################
##################################################################################
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

