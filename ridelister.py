# Ridelister top level program.   
# Notes on sub-division 
#  

import os
import urllib

import cgi 
import jinja2
import webapp2

from bob.submissions import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
	    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
	template = JINJA_ENVIRONMENT.get_template('index.html')
	self.response.write(template.render())

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/submit', SubmissionReport),
], debug=True)



