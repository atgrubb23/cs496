from libraries import *
from basePage import *

class Admin(BaseHandler):
	def __init__(self, request, response):
		self.initialize(request, response)
		self.templateValues = {}
		self.templateValues['uploadUrl'] = blobstore.create_upload_url( '/location/add' )

	# render for self.render within this file
	def render(self, page):
		#self.templateValues['comments'] = [{'date': i.date, 'body': i.body, 'key': i.key.urlsafe()} for i in Comment.query().fetch()]
		self.templateValues['locations'] = [{'name': i.name, 'key':i.key.urlsafe()} for i in Location.query(ancestor = ndb.Key(Location, self.app.config.get('default-group'))).fetch()]
		BaseHandler.render(self, page, self.templateValues)

	def get(self):
		self.render('admin.html')

	def post(self, icon_key = None):
		action = self.request.get('action')
		if action == 'addLocation':
			key = ndb.Key(Location, self.app.config.get('default-group'))
			location = Location(parent = key)
			location.name = self.request.get('locationName')
			if self.request.get('locationActive') == 'active':
				location.active = True
			else:
				location.active = False
			location.rating = int(self.request.get('rating'))
			location.image = str(icon_key)
			location.put()
			self.templateValues['message'] = 'Added location ' + location.name + '.'
		else:
			self.templateValues['message'] = 'Undefined action.'

		self.render('admin.html')

class AddLocation(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		uploadFiles = self.get_uploads('image')
		if uploadFiles != []:
			blob_info = uploadFiles[0]
			Admin(self.request, self.response).post(icon_key = blob_info.key())
		else:
			Admin(self.request, self.response).post()

class EditLocation(blobstore_handlers.BlobstoreUploadHandler):
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
		'''
		commentBoxes = []
		for c in comments:
			if c.key in location.comments:
				commentBoxes.append({'body': c.body, 'date': c.date})
			else:
				commentBoxes.append({'name': })
		'''
		self.render('edit.html', self.templateValues)

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