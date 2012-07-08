import random

import questionlist

class QuestionType:
	BestAnswer = 'bestAnswer';
	AllThatApply = 'allThatApply';
	AgreeOrDisagree = 'agreeOrDisagree';
	
class AnswerOrderType:
	Constant = 'constant';
	Shuffle = 'shuffle';
	RandomReverse = 'randomReverse';
	
class Question(object):
	def __init__(self, id, text, answers=None, type=QuestionType.BestAnswer, tags=[], answer_order_type=AnswerOrderType.Shuffle):
		self.id = id;
		self.text = text;
		self.answers = answers;
		self.type = type;
		self.tags = tags;
		self.answer_order_type = answer_order_type;
		
		if self.is_agree_or_disagree and self.answers == None:
			self.answers = [ 'Strongly disagree', 'Disagree', 'Neither agree nor disagree', 'Agree', 'Strongly agree' ];
			self.answer_order_type = AnswerOrderType.RandomReverse;
		
	@property
	def is_best_answer(self):
		return self.type == QuestionType.BestAnswer;
		
	@property
	def is_all_that_apply(self):
		return self.type == QuestionType.AllThatApply;
		
	@property
	def is_agree_or_disagree(self):
		return self.type == QuestionType.AgreeOrDisagree;
		
	@property
	def randomized_answers(self):
		answers_and_indices = zip(self.answers, range(0, len(self.answers)));
		if self.answer_order_type == AnswerOrderType.Constant:
			pass;
		elif self.answer_order_type == AnswerOrderType.Shuffle:
			random.shuffle(answers_and_indices);
		elif self.answer_order_type == AnswerOrderType.RandomReverse:
			if random.choice((True, False)):
				answers_and_indices.reverse();
		return answers_and_indices;
					
__all = None;
def all():
	global __all;
	if __all is None:
		__all = questionlist.all();
	return __all;

__all_by_id = None;
def all_by_id():
	global __all_by_id;
	if __all_by_id is None:
		__all_by_id = dict([(question.id, question) for question in all()]);
	return __all_by_id;