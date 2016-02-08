# Functions for sending email to users.
# Centralized because it makes more sense that way
# Assume that they have credentials.

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

from ridelib.config import *

# The email message they get when they submit the listing.
def email_submission_confirm(key):
    # Now that we've sent the form response, send the confirmation email.
    # There should have been a checkbox in case they didn't want it.

    ridelisting = key.get()

    user = users.get_current_user()

    message = mail.EmailMessage(sender="Ride Lister <robert@kudra.com>",
                                    subject="Your ride listing")
    message.to = user.email()

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
  
    message.send()

# This is what you get when your listing is approved.
def email_publication_approved(key):
    # Now that we've sent the form response, send the confirmation email.
    # There should have been a checkbox in case they didn't want it.

    
    ridelisting = key.get()

    message = mail.EmailMessage(sender="Ride Lister <robert@kudra.com>",
                                    subject="Your ride listing was approved")

    # Need some code here to look up the submitter's email address and 
    # Address it correctly.

    message.to = ridelisting.submitter_email
    message.body = """

Your ride listing has been approved and has been published

<p>Ride Name: %s
<p>Ride Starting Location: %s
<p>Ride Description: %s

<p>If you need to cancel this ride, please do so here: <a href="cancel?dbkey=%s">Edit</a>
<p>If you would like to re-use this ride listing, go here: <a href="resubmit?dbkey=%s">Edit</a>

    """ % (
        ridelisting.name,
        ridelisting.startlocation,
        ridelisting.description,
        key.urlsafe(),key.urlsafe()
        )
        
    message.send()



