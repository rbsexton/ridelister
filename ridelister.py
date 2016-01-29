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
    'secret_key': '242334c07588e6fcf93551e1c5bdefc3',
}

app = webapp2.WSGIApplication([
    ('/', RideEntry),
    ('/edit', RideEntryEdit),
    ('/submit', SubmissionAck),
    ('/view', SubmissionDisplay),
    ('/approve', SubmissionApprove),
], config=config, debug=True)



