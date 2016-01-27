'''
Methods Related to processing approvals.
All of these will require validation
'''
__all__ = (
    "SubmissionApprove",
    "SubmissionReject",
    "AdminRideCancel",
)

import os
import jinja2
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class SubmissionApprove(webapp2.RequestHandler):
    def get(self):
    
        # Get Credentials
        user = users.get_current_user()

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

