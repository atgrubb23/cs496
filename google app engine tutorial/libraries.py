import webapp2
import jinja2
import os
import datetime
import cgi
import urllib
import unicodedata

from google.appengine.api import images
from google.appengine.api import users
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from ndb_definitions import *