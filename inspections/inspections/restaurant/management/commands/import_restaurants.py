import json

from django.core.management.base import BaseCommand

from inspections.restaurant.models import Restaurant

class Command(BaseCommand):

	restaurants = []

	def clear_old_data(self):
		"""
		Start from scratch when we run this management command.
		"""
		print '1. Clearing %s objects.' % Restaurant.objects.all().count()
		
		Restaurant.objects.all().delete()

	def read_json(self):
		"""
		Reads JSON list of restaurants into a class attribute.
		"""
		print '2. Loading restaurant_list.json'
		
		with open('data/restaurant_list.json', 'rb') as jsonfile:
			self.restaurants = json.loads(jsonfile.read())

	def insert_restaurants(self):
		"""
		Loops over list of restaurants and inserts them into the DB.
		"""
		print '3. Loaded %s restaurants from the JSON.' % len(self.restaurants)

		print '4. Loading restaurants into the DB.'

		for restaurant in self.restaurants:

			# Our data set uses a reserved word as a key. Let's fix that.
			restaurant['restaurant_type'] = restaurant['type']
			restaurant.pop('type')

			# The ** notation unpacks this dictionary into keyword arguments
			# aka kwargs. The ravenous kwarg is very dangerous, so handle with
			# care. This works great if the keys in the dictionary completely
			# match the model attributes.
			r = Restaurant(**restaurant)

			r.save()

			print '\t+ %s' % r

	def handle(self, *args, **options):
		"""
		Invoked when the management command is run.
		"""
		self.clear_old_data()
		self.read_json()
		self.insert_restaurants()
