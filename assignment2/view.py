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
			self.templateValues['img_url'] = images.get_serving_url(location.image, crop = True, size = 64)
		self.templateValues['location'] = location
		self.templateValues['key'] = location.key.urlsafe()
		'''
		commentBoxes = []
		for c in comments:
			if c.key in location.comments:
				commentBoxes.append({'body': c.body, 'date': c.date})
			else:
				commentBoxes.append({'name': })
		'''
		self.render('view.html', self.templateValues)