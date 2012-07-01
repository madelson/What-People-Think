class QuestionType:
	BestAnswer = 1;
	AllThatApply = 2;

class Question(object):
	def __init__(self, id, text, answers, type=QuestionType.BestAnswer, tags=[]):
		self.id = id;
		self.text = text;
		self.answers = answers;
		self.type = type;
		self.tags = tags;

# contains all questions in Wyvern
all = [
	Question(
		id="1", 
		text="What is your favorite color",
		answers=["red", "green", "blue", "other"],
	),
	Question(
		id="2", 
		text="What is your favorite number",
		answers=["1", "2", "3", "7", "other"],
	),
];