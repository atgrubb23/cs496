from libraries import *
from basePage import *

class ViewEditLocation(BaseHandler):
	def __init__(self, request, response):
		self.initialize(request,response)
		self.templateValues = {}
		self.templateValues['editUrl'] = blobstore.create_upload_url( '/edit/location' )

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
		self.render('edit.html', self.templateValues)

class EditLocation(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		locationKey = ndb.Key(urlsafe=self.request.get('key'))
		location = locationKey.get()
		if self.request.get('image-action') == 'remove':
			channel.image = None
		elif self.request.get('image-action') == 'change':
			uploadFiles = self.get_uploads('image')
			if uploadFiles != []:
				blob_info = uploadFiles[0]
				location.image = blob_info.key()
		location.put()
		self.redirect('/edit?key=' + locationKey.urlsafe())