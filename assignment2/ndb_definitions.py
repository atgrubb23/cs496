from google.appengine.ext import ndb

class Location(ndb.Model):
	# Class that repesents pick up game locations
	name = ndb.StringProperty(required=True)
	description = ndb.StringProperty(required=False)
	active = ndb.BooleanProperty(required=False)
	image = ndb.BlobProperty(required=False)
	rating = ndb.IntegerProperty(required=False)