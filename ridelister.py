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

config = {}
config['webapp2_extras.sessions'] = {
    'secret_key': 'ridelister242334c0',
    'cookie_name': 'ridelister-session',
}

app = webapp2.WSGIApplication([
    ('/', RideEntry),
    ('/edit', RideEntryEdit),
    ('/submit', SubmissionAck),
    ('/view', SubmissionDisplay),
    ('/oauth2callback', SubmissionGoogleAuth),
    ('/approve', SubmissionApprove),
], config=config, debug=True)



