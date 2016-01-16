'''This is some documentation'''
__all__ = (
	"SubmissionReport",
)

import cgi 
import webapp2

class SubmissionReport(webapp2.RequestHandler):
    def post(self):
	    self.response.write('<html><body>Your Ride:<pre>')
	    self.response.write(cgi.escape(self.request.get('title')))
	    self.response.write('</pre></body></html>')

def bar(x):
	return x + 1
	