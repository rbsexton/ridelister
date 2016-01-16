# ridelister
Google Appengine-based bike club ride listing system

Basic FLow
- User lands on / -> RideEntry(webapp2.RequestHandler)
- POST Occurs, and the data is delivered to /submit -> SubmissionReport(webapp2.RequestHandler)
-- SubmissionReport adds a ndb item, displays the info for the user, and sends off emails to the 
   submitter of the ride (if they are logged in) and the ride approvers.

- The Ride approvers get an email with a link.   That should take them to a form that 
  displays the ride data and gives them a change to make changes prior to approval, or rejection.

Other things 

Google calendar events can generate change notifications that take the form of http requests.  Something
needs to respond to those and send out an updated notification.

Google Drive can serve as a container for cue sheets, etc.



