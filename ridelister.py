# Ridelister top level program.   
# Notes on sub-division 
#  

import os
import urllib

import cgi 
import jinja2
import webapp2

from ridelib.submissions import *
from ridelib.rideentry import *

app = webapp2.WSGIApplication([
	('/', RideEntry),
	('/submit', SubmissionReport),
	('/view', SubmissionDisplay),
], debug=True)



