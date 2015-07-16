from libraries import *
from basePage import *

class View(BaseHandler):
	def __init__(self, request, response):
		self.initialize(request,response)
		self.templateValues = {}	

	def get(self):
		locationKey = ndb.Key(urlsafe=self.request.get('key'))
		location = locationKey.get()
		if location.image:
			self.templateValues['img_url'] = images.get_serving_url(location.image)
		self.templateValues['location'] = location
		self.templateValues['key'] = location.key.urlsafe()
		self.render('view.html', self.templateValues)