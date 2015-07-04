import 
class MainPage(webapp2.RequestHandler):
    def get(self):
    	user = users.get_current_user()

    	if user:
    		url = users.create_logout_url(self.redirect.uri)
    		url_linktext = 'Logout'

    	else:
    		url = users.create_login_url(self.redirect.uri)
    		url_linktext = 'Login'

    	