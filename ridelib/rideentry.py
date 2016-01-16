'''Put up the initial form for entering the ride.  Pretty basic.'''
__all__ = (
    "RideEntry",
)

import os
import jinja2
import webapp2

from google.appengine.api import users

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)

class RideEntry(webapp2.RequestHandler):
    def get(self):
    
        user = users.get_current_user()

        if user:
            greeting = 'Hello, ' + user.nickname()
        else:
            greeting = 'You are not logged into google.  Some features will be unavailable'
            self.redirect(users.create_login_url(self.request.uri))
        
        template_values = {
            'greeting': greeting,
            }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))


