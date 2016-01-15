import os
import urllib

import cgi 
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
	    autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
	template = JINJA_ENVIRONMENT.get_template('index.html')
	self.response.write(template.render())

class SubmissionReport(webapp2.RequestHandler):
    def post(self):
	    self.response.write('<html><body>Your Ride:<pre>')
	    self.response.write(cgi.escape(self.request.get('title')))
	    self.response.write('</pre></body></html>')

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/submit', SubmissionReport),
], debug=True)

