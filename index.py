import webapp2
import jinja2
import os
import datetime
import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_NAME = 'Default Location'

def locationKey(locationName = DEFAULT_NAME):
    # Constructs a Datastore key for a location.
    # locationName is the key.
    return ndb.Key('Location', locationName)

class Commentor(ndb.Model):
	# Class that represents users who author comments
	identity = ndb.StringProperty(indexed=False)
	email = ndb.StringProperty(indexed=False)

class Comment(ndb.Model):
	# Class representing user comments
	commentor = ndb.StructuredProperty(Commentor)
	date = ndb.DateTimeProperty(auto_now_add=True) # Gives the object a datetime stamp corresponding to when it was created
	body = ndb.StringProperty(indexed=False)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.write('<html><body>')
        locationName = self.request.get('locationName', DEFAULT_NAME)

        # Ancestor Queries, as shown here, are strongly consistent
        # with the High Replication Datastore. Queries that span
        # entity groups are eventually consistent. If we omitted the
        # ancestor from this query there would be a slight chance that
        # Greeting that had just been written would not show up in a
        # query.
        commentsQuery = Comment.query(ancestor = locationKey(locationName)).order(-Comment.date)
        comments = commentsQuery.fetch(100)

        # Get current user object and store in a var
        user = users.get_current_user()

        if user:
        	url = users.create_logout_url(self.request.uri)
        	url_linktext = 'Logout'

        else:
        	url = users.create_login_url(self.request.uri)
        	url_linktext = 'Login'

        templateValues = {
        	'user': user,
        	'comments': comments,
        	'locationName': urllib.quote_plus(locationName),
        	'url': url,
        	'url_linktext': url_linktext
        }
        template = JINJA_ENVIRONMENT.get_template('/templates/index.html')

        self.response.write(template.render(templateValues))

class LocationComments(webapp2.RequestHandler):
    def post(self):
        locationName = self.request.get('locationName', DEFAULT_NAME)

        # By assigning the parent this assigns all comments of a particular Location to the same entity group
        # by setting the same parent for each comment. 
        # Limited 1 write per second. 
        # !!!USE MEMCACHE SEE LECTURES!!!
        comment = Comment(parent = locationKey(locationName))

        if users.get_current_user():
        	comment.commentor = Commentor(identity = users.get_current_user().user_id(), 
        		email = users.get_current_user().email())

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        comment.body = self.request.get('body') # Store the body of the comment
        comment.put() # Write the comment obj to the datastore

        queryParams = {'locationName': locationName}
        self.redirect('/?' + urllib.urlencode(queryParams))