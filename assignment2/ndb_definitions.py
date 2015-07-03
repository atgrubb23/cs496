from google.appengine.ext import ndb

class Location(ndb.Model):
	# Class that repesents pick up game locations
	name = ndb.StringProperty(required=True)
	comments = ndb.KeyProperty(repeated=True)
	active = ndb.BooleanProperty(required=False)
	image = ndb.BlobProperty(required=False)
	rating = ndb.IntegerProperty(required=False)

class Author(ndb.Model):
	# Class that represents users who author comments
	identity = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty(indexed=False)

class Comment(ndb.Model):
	# Class representing user comments
	author = ndb.StructuredProperty(Author)
	date = ndb.DateTimeProperty(auto_now_add=True) # Gives the object a datetime stamp corresponding to when it was created
	body = ndb.StringProperty(indexed=False)