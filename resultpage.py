import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import question
import entities
import random
import logging
#import index

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# presents the result of a question to the user
class ResultPage(webapp.RequestHandler):
	def get(self, question_id):
		print 'hi: "' + str(question_id) + '"';