class QuestionType:
	BestAnswer = 1;
	AllThatApply = 2;
	
class Question(object):
	def __init__(self, id, text, answers, type=QuestionType.BestAnswer, tags=[], preserve_answer_order=False):
		self.id = id;
		self.text = text;
		self.answers = answers;
		self.type = type;
		self.tags = tags;
		self.preserve_answer_order = preserve_answer_order;

# contains all questions in Wyvern
all = [
	Question(
		id="1", 
		text="What is your favorite color?",
		answers=["red", "green", "blue", "other"],
	),
	Question(
		id="2", 
		text="What is your favorite number?",
		answers=["1", "2", "3", "7", "other"],
	),
	Question(
		id="3",
		text="Where do you tend to fall politically?",
		answers=[
			"Economically liberal, socially liberal",
			"Economically liberal, socially conservative",
			"Economically conservative, socially liberal",
			"Economically conservative, socially conservative"
		],
		tags=["Politics"]
	),
	Question(
		id="4",
		text="Which of the following questions do you think is most important when forming an opinion about abortion?",
		answers=[
			"When, exactly, in the development process an embryo becomes a human being",			
		],
		tags=["Morality"]
	),
	Question(
		id="5",
		text="""
			Which of the following arguments about <a href='http://en.wikipedia.org/wiki/Inheritance'>inheritance</a> 
			do you agree with more?
		""",
		answers=[
			"As long as inheritance is allowed, the world will never be fair because there can never be equality of opportunity",
			"Disallowing inheritance is unfair because people should be able to give their property to whomever they chose"
		],
		tags=["Morality", "Economics"]
	),
	Question(
		id="6",
		text="Do you believe that access to health care is:",
		answers=[
			"A necessity?",
			"A luxury?"		
		],
		tags=["Politics", "Economics", "Morality"]
	)
];

all_by_id = dict([(question.id, question) for question in all]);