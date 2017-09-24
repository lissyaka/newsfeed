import re

class SlugGenerator:

	def __init__(self, title):
		self.title = title

	def generate(self):
		slug = self.title.lower()
		slug = re.sub("[^a-zA-Z0-9 ]+", "", slug)
		slug = re.sub("[^a-zA-Z0-9]+", "-", slug)
		return slug
