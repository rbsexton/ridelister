# Ridelister top level program.   
# Notes on sub-division 
#  

import os
import urllib

import cgi 
import jinja2
import webapp2

from bob.submissions import *
from bob.ridedata import *
from bob.rideentry import *

app = webapp2.WSGIApplication([
	('/', RideEntry),
	('/submit', SubmissionReport),
], debug=True)



