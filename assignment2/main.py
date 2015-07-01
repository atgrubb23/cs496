import webapp2

app = webapp2.WSGIApplication([
	('/', 'index.MainPage'),
	('/sign', 'index.LocationComments')
	], debug=True)
