# Ridelister top level program.   
# Notes on sub-division 
#  

import os
import urllib

import cgi 
import jinja2
import webapp2

from ridelib.rideentry import *
from ridelib.submit import *
from ridelib.approver import *

app = webapp2.WSGIApplication([
    ('/', RideEntry),
    ('/edit', RideEntryEdit),
    ('/submit', SubmissionAck),
    ('/view', SubmissionDisplay),
    ('/approve', SubmissionApprove),
], debug=True)



