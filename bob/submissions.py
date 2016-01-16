'''Code to handle submission of the http post'''
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

class SubmissionReport(webapp2.RequestHandler):
    def post(self):
        ridename = cgi.escape(self.request.get('name'))
        ridestart = cgi.escape(self.request.get('startinglocation'))
        ridedescription = cgi.escape(self.request.get('description'))
    
        template_values = {
			'ridename': ridename,
			'ridestart': ridestart,
			'ridedescription': ridedescription
        }
    
        template = JINJA_ENVIRONMENT.get_template('submissionack.html')
        self.response.write(template.render(template_values))

