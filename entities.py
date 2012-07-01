from google.appengine.ext import db
import random;

class Answerer(db.Model):
	questions_answered = db.StringListProperty();
	answers = db.StringListProperty();

class CounterShard(db.Model):
	count = db.IntegerProperty(required=True, default=0);
	counter_kind = db.StringProperty(required=True);

# based on http://code.google.com/p/google-app-engine-samples/source/browse/trunk/sharded-counters/generalcounter.py
class ShardedCounter(object):
	SHARD_COUNT = 10;
	
	def __init__(self, counter_kind):
		self.counter_kind = counter_kind;

	def value(self):
		total = 0;
		total_count_query = db.GqlQuery("""
			SELECT count
			FROM CounterShard
			WHERE counter_kind = :counter_kind
			""",
			counter_kind=self.counter_kind
		);
		for proj in total_count_query:
			total += proj.count;
		return total;
	
	def increment(self, value = 1):		
		def transaction():
			index = random.randint(0, ShardedCounter.SHARD_COUNT - 1);
			shard_name = self.counter_kind + ':' + str(index);
			counter = CounterShard.get_by_key_name(shard_name);
			if counter is None:
				counter = CounterShard(key_name=shard_name, counter_kind = self.counter_kind);
			counter.count += value;
			counter.put();
			
		db.run_in_transaction(transaction);
	
