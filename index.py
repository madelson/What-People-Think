import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import question
import entities
import random
import logging
import resultpage
import questionpage
import handlers

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
				
application = webapp.WSGIApplication([
	('/(\w*)', questionpage.QuestionPage),
	('/ask/(\w*)', questionpage.QuestionPage),
	('/result/(\w+)', resultpage.ResultPage)
], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()