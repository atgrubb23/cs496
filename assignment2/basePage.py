from libraries import *

class BaseHandler(webapp2.RequestHandler):
	@webapp2.cached_property
	def jinja2(self):
		return jinja2.Environment(
			loader = jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
			extensions = ['jinja2.ext.autoescape'],
			autoescape = True
		)

	def render(self, template, templateVariables={}):
		template = self.jinja2.get_template(template)
		self.response.write(template.render(templateVariables))