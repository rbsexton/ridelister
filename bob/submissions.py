'''
Code to handle submission of the http posts.
SubmissionReport handles the initial user submission.

'''
__all__ = (
    "SubmissionReport",
)

import os
import jinja2

import cgi 
import webapp2
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

from bob.ridedata import *

class SubmissionReport(webapp2.RequestHandler):
    def post(self):
        ridename = cgi.escape(self.request.get('name'))
        ridestart = cgi.escape(self.request.get('startinglocation'))
        ridedescription = cgi.escape(self.request.get('description'))

        # Load it up into a NDB entry.
        listing = RideDataItem(
            name = ridename,
            startlocation = ridestart,
            description = ridedescription,
            )

        # Now its time to stash this data into the database and retrieve the key
        # So that it can be handed off.
        
        key = listing.put()
        ridedbkey = key.urlsafe()
    
        template_values = {
            'ridename': ridename,
            'ridestart': ridestart,
            'ridedescription': ridedescription,
            'ridedbkey': ridedbkey,
        }

        template = JINJA_ENVIRONMENT.get_template('submissionack.html')
        self.response.write(template.render(template_values))





