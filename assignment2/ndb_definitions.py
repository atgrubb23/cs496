from google.appengine.ext import ndb

class Model(ndb.Model):
	def to_dict(self):
		d = super(Model, self).to_dict()
		d['key'] = self.key.id()
		return d

class Comment(ndb.Model):
	# Class that represents a comment
	author = ndb.StringProperty(required=True)
	body = ndb.StringProperty()
	timestamp = ndb.DateTimeProperty(auto_now_add=True)

class Location(ndb.Model):
	# Class that repesents pick up game locations
	name = ndb.StringProperty(required=True)
	description = ndb.StringProperty()
	active = ndb.BooleanProperty()
	image = ndb.BlobProperty()
	rating = ndb.IntegerProperty()
	comments = ndb.StructuredProperty(Comment, repeated=True)

	def to_dict(self):
		all_comments = {}
		a = 1
		for c in self.comments:
			all_comments['comment' + str(a)] = {"author": c.author, "body": c.body, "timestamp": str(c.timestamp)}
			a += 1

		return {
			'id': self.key.id(),
			'name': self.name,
			'description': self.description,
			'active': self.active,
			'image': self.image,
			'rating': self.rating,
			'comments': all_comments
		}

class User(ndb.Model):
	# Class that represents users who will utilize locations
	name = ndb.StringProperty(required=True)
	email = ndb.StringProperty(required=True)
	image = ndb.BlobProperty()
	sports = ndb.StringProperty(repeated=True)
	rating = ndb.IntegerProperty()
	#comments = ndb.StructuredProperty(Comment, required=False, repeated=True)