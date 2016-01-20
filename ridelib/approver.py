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

class SubmissionApprove(webapp2.RequestHandler):
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

