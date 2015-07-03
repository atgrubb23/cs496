from libraries import *

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

DEFAULT_NAME = 'Default Location'

def locationKey(locationName = DEFAULT_NAME):
    # Constructs a Datastore key for a location.
    # locationName is the key.
    return ndb.Key('Location', locationName)

class LocationPage(webapp2.RequestHandler):
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
        locationQuery = Location.query(ancestor=ndb.Key('Location', 'base-data'))
        locationComments = locationQuery.fetch()

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
            'locationName': urllib.unquote_plus(locationName),
            'url': url,
            'url_linktext': url_linktext,
            'locations': [{'name':loc.name} for loc in Location.query().fetch()]
        }

        template = JINJA_ENVIRONMENT.get_template('/templates/location.html')
        self.response.write(template.render(templateValues))

class LocationComments(webapp2.RequestHandler):
    def post(self):
        locationName = self.request.get('locationName', DEFAULT_NAME)

        # By assigning the parent this assigns all comments of a particular Location to the same entity group
        # by setting the same parent for each comment. 
        # Limited 1 write per second. (from Google Documentation)
        comment = Comment(parent = locationKey(locationName))

        if users.get_current_user():
            comment.commentor = Commentor(identity = users.get_current_user().user_id(), 
                email = users.get_current_user().email())

        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        comment.body = self.request.get('body') # Store the body of the comment
        comment.put() # Write the comment obj to the datastore

        key = ndb.Key('Location', 'base-data')
        location = Location(parent = key)
        location.name = locationName
        location.put()

        queryParams = {'locationName': locationName}
        self.redirect('/?' + urllib.urlencode(queryParams))

#class AddLocation():
    #def get(self):