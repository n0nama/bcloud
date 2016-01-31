from haystack import indexes
from users.models import Profile

class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True, template_name='search/indexes/users/profile_text.txt')
	author = indexes.CharField(model_attr='user')
	f_name = indexes.CharField(model_attr='f_name')
	l_name = indexes.CharField(model_attr='l_name')
	
	def get_model(self):
		return Profile