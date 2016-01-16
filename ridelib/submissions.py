'''
Code to handle submission of the http posts.
SubmissionReport handles the initial user submission.

'''
__all__ = (
    "SubmissionReport",
    "SubmissionDisplay",
)

import os
import jinja2

import cgi 
import webapp2
import jinja2

from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

from ridelib.ridedata import *

class SubmissionReport(webapp2.RequestHandler):
    def post(self):
        ridename = cgi.escape(self.request.get('name'))
        ridestart = cgi.escape(self.request.get('startinglocation'))
        ridedescription = cgi.escape(self.request.get('description'))

        # Load it up into a NDB entry.
        listing = RideDataItem(
			version = 1,
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



# Here is a class that can be used to display a database entry.
class SubmissionDisplay(webapp2.RequestHandler):
    def get(self):
        textkey = self.request.get('dbkey')

        # There should be some error checking here.
   
        entrykey = ndb.Key(urlsafe=textkey)        
        ridelisting = entrykey.get()
       
        template_values = {
            'ridename': ridelisting.name,
			'ridestart': ridelisting.startlocation,
			'ridedescription': ridelisting.description,
			'creation': ridelisting.created,
			'modified': ridelisting.modified,
            'ridedbkey': textkey,
        }
 
        template = JINJA_ENVIRONMENT.get_template('submissionview.html')
        self.response.write(template.render(template_values))

# For future use.
class SubmissionDisplayAll(webapp2.RequestHandler):
    def get(self):
         self.response.write('<html><body>Placeholder</html></body>')














