import cgi
import datetime
import urllib
import wsgiref.handlers
import os
import question
import entities
import random
import logging

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# gets template values to be populated across all pages
def get_template_values_common(answerer):
	values = {
		'answerer': answerer
	};
	return values;

# extracts a user id value for the request
def get_user_id(request):
	return str(request.remote_addr);
	
# finds a template for the given name
def template_path(name):
	path = os.path.join(os.path.dirname(__file__), name + '.html');
	return path;

# asks the user a question
class QuestionPage(webapp.RequestHandler):
	def get(self):		
		id = get_user_id(self.request);
		answerer = entities.Answerer.get_or_insert(id);	
		common_values = get_template_values_common(answerer);

		# determine the question to ask
		
		# if the user has answered all questions, redirect
		if len(answerer.questions_answered) == len(question.all):
			self.redirect();
			return;
				
		# if there is a question in the request AND it's valid, use that unless
		# it's already been answered by the user
		requested_question = self.request.get('question');
		if requested_question in answerer.questions_answered:
			self.redirect();
			return;
		if requested_question in question.all_by_id:
			question_to_ask = requested_question;
		else: # otherwise, choose a random question
			already_answered = True;
			while already_answered:
				question_to_ask = question.all[random.randint(0, len(question.all) - 1)].id;
				already_answered = question_to_ask in answerer.questions_answered;					
			
		template_values = {
			'template': template_path('question'),
			'question': question.all_by_id[question_to_ask],
			'dump': {
				'id': get_user_id(self.request),
				'key2': answerer.key().name()
			}
        };

		path = template_path('index');
		self.response.out.write(template.render(path, dict(common_values.items() + template_values.items())));
	
	def post(self):
		id = get_user_id(self.request);
		answerer = entities.Answerer.get_by_key_name(id);
		
		# if no answerer could be found, redirect
		if answerer is None:
			self.redirect();
			return;
		
		# otherwise, record the answer and redirect to the answer page
		question_id = self.request.get('question');
		answer = self.request.get('answer');		
		if (question_id in question.all_by_id 
			and question_id not in answerer.questions_answered
			and 0 <= int(answer) < len(question.all_by_id[question_id].answers)):
			# update the answerer
			answerer.questions_answered.append(question_id);
			answerer.answers.append(answer);
			answerer.put();
			
			# update the answer counter
			counter = entities.ShardedCounter(question_id + ":" + answer);
			counter.increment();
			
		# redirect to the answer page for that question
		self.redirect("/ask?question_id=%s&answer=%s" % (question_id, answer));
		
		
application = webapp.WSGIApplication([
	('/', QuestionPage),
	('/ask', QuestionPage),
	('/answer', QuestionPage)
], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()