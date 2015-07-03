import webapp2

config = {'default-group':'base-data'}
"""
app = webapp2.WSGIApplication([
	('/', 'location.LocationPage'),
	('/comment', 'location.LocationComments')
	], debug=True)
"""
app = webapp2.WSGIApplication([
	('/', 'admin.Admin'),
	('/admin', 'admin.Admin'),
	('/view', 'view.View'),
	('/location/view', 'view.View'),
	('/location/add', 'admin.AddLocation'),
	('/edit', 'edit.ViewEditLocation')
], debug = True, config = config)