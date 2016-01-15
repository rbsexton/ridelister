import webapp2
import cgi

MAIN_PAGE_HTML = """\
<html>
  <body>
      <form action="/submit" method="post">
	<div>Ridename:<textarea name="title" rows="1" cols="60"></textarea></div>
	<div>Starting Location: <textarea name="starting" rows="1" cols="60"></textarea></div>
	<div>Description: <textarea name="description" rows="3" cols="60"></textarea></div>
	<div><input type="submit" value="Submit"></div>
      </form>
</body>
</html>
"""

class MainPage(webapp2.RequestHandler):
    def get(self):
    	self.response.write(MAIN_PAGE_HTML)

class SubmissionReport(webapp2.RequestHandler):
    def post(self):
	    self.response.write('<html><body>Your Ride:<pre>')
	    self.response.write(cgi.escape(self.request.get('title')))
	    self.response.write('</pre></body></html>')

app = webapp2.WSGIApplication([
	('/', MainPage),
	('/submit', SubmissionReport),
], debug=True)

