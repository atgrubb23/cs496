from libraries import *
from basePage import *

class ViewEditLocation(BaseHandler):
	def __init__(self, request, response):
		self.initialize(request,response)
		self.templateValues = {}
		self.templateValues['editUrl'] = blobstore.create_upload_url( '/location/edit' )

	def get(self):
		locationKey = ndb.Key(urlsafe=self.request.get('key'))
		location = locationKey.get()
		if location.image:
			self.templateValues['img_url'] = images.get_serving_url(location.image)
		self.templateValues['location'] = location
		self.templateValues['key'] = location.key.urlsafe()
		self.render('edit.html', self.templateValues)

class EditLocation(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		locationKey = ndb.Key(urlsafe=self.request.get('key'))
		location = locationKey.get()
		location.name = self.request.get('locationName')
		if self.request.get('locationActive') == 'active':
			location.active = True
		else:
			location.active = False
		location.rating = int(self.request.get('rating'))
		location.description = str(self.request.get('description'))
		if self.request.get('image-action') == 'remove':
			location.image = None
		elif self.request.get('image-action') == 'change':
			uploadFiles = self.get_uploads('image')
			if uploadFiles != []:
				blob_info = uploadFiles[0]
				location.image = str(blob_info.key())
		location.put()
		self.redirect('/edit?key=' + locationKey.urlsafe())