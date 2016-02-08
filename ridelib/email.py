# Functions for sending email to users.
# Centralized because it makes more sense that way
# Assume that they have credentials.

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

from ridelib.config import *

def email_submission_confirm(key):
    # Now that we've sent the form response, send the confirmation email.
    # There should have been a checkbox in case they didn't want it.

    
    ridelisting = key.get()

    message = mail.EmailMessage(sender="Ride Lister <robert@kudra.com>",
                                    subject="Your ride listing")

    message.body = """

Thanks for submitting your ride!

<p>Ride Name: %s
<p>Ride Starting Location: %s
<p>Ride Description: %s

<p>You may edit this ride listing: <a href="edit?dbkey=%s">Edit</a>

    """ % (
        ridelisting.name,
        ridelisting.startlocation,
        ridelisting.description,
        key.urlsafe()
        )
        
        