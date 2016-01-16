'''Put up the initial form for entering the ride.  Pretty basic.'''
__all__ = (
	"RideEntry",
)

import os
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
	    autoescape=True)

class RideEntry(webapp2.RequestHandler):
    def get(self):
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render())
