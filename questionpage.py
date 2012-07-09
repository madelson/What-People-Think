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
import handlers

from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

# asks the user a question
class QuestionPage(webapp.RequestHandler):
	# ask the user a question
	def get(self, question_id):		
		id = handlers.get_user_id(self.request);
		answerer = entities.Answerer.get_or_insert(id);	
		common_values = handlers.get_template_values_common(answerer);
		
		# if no question_id was passed, pick a random question and redirect to that
		if question_id is None or question_id == '':
			already_answered = True;
			while already_answered:
				question_to_ask = question.all()[random.randint(0, len(question.all()) - 1)].id;
				already_answered = question_to_ask in answerer.questions_answered;					
			self.redirect('/ask/%s' % question_to_ask);
			return;
	
		# error out on an invalid id since that's an invalid URL
		if question_id not in question.all_by_id():
			return handlers.bad_request_error(self, 'Invalid question identifier "%s"' % question_id);
	
		# determine the question to ask
		
		# if the user has answered all questions, redirect
		if len(answerer.questions_answered) == len(question.all()):
			self.redirect(); # TODO implement
			return;
					
		# if they already answered the question, redirect to the result page
		if question_id in answerer.questions_answered:
			self.redirect('/result/%s' % question_id);
			return;
			
		template_values = {
			'template': handlers.template_path('question'),
			'question': question.all_by_id()[question_id],
			'dump': {
				'id': handlers.get_user_id(self.request),
				'key2': answerer.key().name()
			}
        };

		path = handlers.template_path('index');
		self.response.out.write(template.render(path, dict(common_values.items() + template_values.items())));
	
	def post(self, question_id):
		# check the question
		if question_id not in question.all_by_id():
			return handlers.bad_request_error(self, 'Invalid question "%s"' % question_id);

		id = handlers.get_user_id(self.request);
		answerer = entities.Answerer.get_by_key_name(id);
		
		# check the answerer
		if answerer is None:
			return handlers.bad_request_error(self, 'Could not identify answerer "%s"' % id);
		# if they've already answered, just redirect
		if question_id in answerer.questions_answered:
			self.redirect('/result/%s' % question_id);
			return;
		# check the answer
		answer = self.request.get('answer');		
		if int(answer) not in range(0, len(question.all_by_id()[question_id].answers)):
			return handlers.bad_request_error(self, 'Invalid answer "%s" for question "%s"' % (answer, question_id)); 
		
		# otherwise, record the answer and redirect to the answer page
		# update the answerer
		answerer.questions_answered.append(question_id);
		answerer.answers.append(answer);
		answerer.put();
		
		# update the answer counter
		counter = entities.ShardedCounter(question_id + ':' + answer);
		counter.increment();
			
		# redirect to the answer page for that question
		self.redirect("/ask/%s" % question_id);