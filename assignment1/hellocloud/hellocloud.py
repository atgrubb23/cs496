import webapp2
import datetime

class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write(datetime.datetime.now())

app = webapp2.WSGIApplication([
	('/', MainPage),
], debug=True)