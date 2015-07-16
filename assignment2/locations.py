from libraries import *
from basePage import *
import ndb_definitions
import json
from google.appengine.ext import ndb

class Locations(BaseHandler):
	def get(self, **args):
		# Return existing Location entities
		if 'application/json' not in self.request.accept:
			self.response.status = 400
			self.respone.status_message = 'ONLY application/json is supported.'
			return
		if 'lid' in args:
			loc = ndb.Key(ndb_definitions.Location, int(args['lid'])).get().to_dict()
			self.response.write(json.dumps(loc))
			self.response.write('\n')
		else:
			query = ndb_definitions.Location.query()
			locations = query.fetch()
			results = []
			for l in locations:
				results.append(l.to_dict())
			self.response.write(json.dumps(results))
			self.response.write('\n')

	def post(self):
		# Make new Location entities
		if 'application/json' not in self.request.accept:
			self.response.status = 400
			self.response.status_message = 'ONLY application/json is supported.'
			self.response.write('ONLY application/json is supported.\n')
			return

		else:
			new_loc = ndb_definitions.Location()
			name = self.request.get('name', default_value=None)
			description = self.request.get('description', default_value=None)
			image = self.request.get('image', default_value=None)
			rating = self.request.get('rating', default_value=None)
			comments = []
			jsonstring = self.request.body
			location_obj = None
			try:
				location_obj = json.loads(jsonstring)
			except:
				# No JSON provided, move along
				pass

			# If POST received with a json string provided, behave accordingly
			if location_obj is not None:
				if 'name' not in location_obj:
					self.response.status = 400
					self.response.status_message = 'Invalid request - a name is required for a POST.'
					self.response.write('Invalid request - a name is required for a POST.\n')
					return
				else:
					name = location_obj['name']
				if 'description' in location_obj:
					description = location_obj['description']
				if 'image' in location_obj:
					image = location_obj['image']
				if 'rating' in location_obj:
					rating = int(location_obj['rating'])
				if 'comments' in location_obj:
					for all_comments, comment in location_obj['comments'].iteritems():
						key = ndb.Key(Comment, self.app.config.get('default-group'))
						a_comment = Comment(parent = key)
						a_comment.author = comment['author']
						a_comment.body = comment['body']
						comments.append(a_comment)
			if name:
				new_loc.name = name
			else:
				self.response.status = 400
				self.response.status_message = 'Invalid request - a name is required for a POST.'
				self.response.write('Invalid request - a name is required for a POST.\n')
				return

			if description:
				new_loc.description = description
			if image:
				new_loc.image = image
			if rating:
				new_loc.rating = rating
			if comments:
				new_loc.comments = comments
			key = new_loc.put()
			self.response.status = 200
			self.response.status_message = 'Successful write to datastore.'
			self.response.write('Successful write to datastore.')
			self.response.write('\n')
			return

	def delete(self, **args):
		# Remove Location entities
		if 'application/json' not in self.request.accept:
			self.response.status = 400
			self.response.status_message = 'ONLY application/json is supported.'
			self.response.write('ONLY application/json is supported.\n')
			return

		else:
			# If ID specified proceed with deletion of Location
			if 'lid' in args:
				#loc = ndb.Key(ndb_definitions.Location, int(args['lid']))
				loc = ndb_definitions.Location.query(ancestor=ndb.Key(Location, int(args['lid'])))
				#location = loc.fetch()
				ndb.delete_multi(loc.fetch(keys_only=True))

				message = 'Location ID: ' + str(args['lid']) + ' has been deleted from datastore.\n'
				self.response.status = 200
				self.response.status_message = message
				self.response.write(message)

			# Cannot remove an entity without an ID specified
			else:
				message = 'Invalid request. An ID must be specified to delete a Location from datastore.\n'
				self.response.status = 400
				self.response.status_message = message
				self.response.write(message)

# For adding/getting comments for Locations
class LocationComments(BaseHandler):
	# Get all comments for a Location entity
	def get(self, **args):
		if 'application/json' not in self.request.accept:
			self.response.status = 400
			self.respone.status_message = 'ONLY application/json is supported.'
			return
		else:
			if 'lid' in args:
				loc = ndb.Key(ndb_definitions.Location, int(args['lid'])).get().to_dict()
				comment = loc['comments']
				#for c in loc['comments']:
				self.response.write(json.dumps(comment))
				self.response.write('\n')
				self.response.write(str(len(comment)))
				self.response.write('\n')
			else:
				message = 'Invalid request. An ID must be specified to retrieve comments for a Location.'
				self.response.status = 400
				self.response.status_message = message
				self.response.write(message)

	# Add new comment to a Location
	# Also can update existing attributes of a Location
	def put(self, **args):
		if 'application/json' not in self.request.accept:
			self.response.status = 400
			self.respone.status_message = 'ONLY application/json is supported.'
			return
		else:
			jsonstring = self.request.body
			location_obj = json.loads(jsonstring)
			loc = ndb.Key(ndb_definitions.Location, int(args['lid'])).get()
			if 'comments' in location_obj:
				for all_comments, comment in location_obj['comments'].iteritems():
					loc.comments.append(comment)
			if 'name' in location_obj:
				loc.name = location_obj['name']
			if 'description' in location_obj:
				loc.description = location_obj['description']
			if 'rating' in location_obj:
				loc.rating = location_obj['rating']
			if 'image' in location_obj:
				loc.image = location_obj['image']
			if 'active' in location_obj:
				loc.active = locatin_obj['active']
			
			loc.put()
			self.response.status = 200
			message = 'Successful update of data store entity ID: ' + str(args['lid']) + '\n'
			self.response.status_message = message
			self.response.write(message)