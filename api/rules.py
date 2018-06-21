from durable.lang import *

with ruleset("suggestedPosts"):

	#User who has been posting a lot recently
	@when_all((m.recentPosts > 0.5))
	def spammer(c):
		c.assert_fact({"userPosting": 0 })

	@when_all((m.recentPosts < 0.5))
	def postingRaking(c):
		c.assert_fact({"userPosting": c.m.recentPosts*100})

	@when_all((m.userRelevance > 0.1))
	def userPopularity(c):
		c.assert_fact({ "userRelevance": c.m.recentPosts*50})

	@when_all((m.userRelevance > 0.3))
	def userPopularity(c):
		c.assert_fact({ "userRelevance": c.m.recentPosts*150})