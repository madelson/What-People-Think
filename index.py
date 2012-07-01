import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import question
import entities

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class MainPage(webapp.RequestHandler):
    def get(self):
		counter1 = entities.ShardedCounter('Type1');
		counter2 = entities.ShardedCounter('Type2');
		for i in range(1, 10):
			counter1.increment();
		for i in range(1, 3):
			counter2.increment();

		template_values = {
			'questions': question.all,
			'dump': {
				'val1': counter1.value(),
				'val2': counter2.value()
			}
        };

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication([
	('/', MainPage)
], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()