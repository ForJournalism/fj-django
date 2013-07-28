import json

from django.core.management.base import BaseCommand
from dateutil.parser import *
from pytz import timezone
import pytz

from inspections.inspection.models import Inspection, Observation
from inspections.restaurant.models import Restaurant

class Command(BaseCommand):

	inspections = []

	def clear_old_data(self):
		"""
		Start from scratch when we run this management command.
		"""
		print '1. Clearing %s inspections and %s observations.' % (Inspection.objects.all().count(), Observation.objects.all().count())
		
		Inspection.objects.all().delete()
		Observation.objects.all().delete()

	def read_json(self):
		"""
		Reads JSON list of inspections into a class attribute.
		"""
		print '2. Loading inspection_list.json'
		
		with open('data/inspection_list.json', 'rb') as jsonfile:
			self.inspections = json.loads(jsonfile.read())

	def insert_inspections(self):
		"""
		Loops over list of inspections and inserts them into the DB.
		Creates observations when they occur and fks to inspection.
		"""
		print '3. Loaded %s inspections from the JSON.' % len(self.inspections)

		print '4. Loading inspections into the DB.'

		for inspection in self.inspections:

			# Our data set uses a reserved word as a key. Let's fix that.
			inspection['inspection_type'] = inspection['type']
			inspection.pop('type')

			# Save the observations to a list.
			# We'll deal with them after we save the inspection.
			# Related items need the relationship to exist first.
			observations = inspection['observations']
			inspection.pop('observations')

			# Save the restaurant permit_id.
			# We'll add the restaurant just before saving.
			restaurant_id = inspection['restaurant']['permit_id']
			restaurant_title = inspection['restaurant']['title']
			inspection.pop('restaurant')

			# Time to deal with datetimes!
			# This is truly the worst thing, ever.
			# First, let's use pytz to set up a timezone.
			# And defend against blank times (will default to midnight, I suspect?).
			eastern = timezone('US/Eastern')
			inspection['time_in'] = eastern.localize(parse(inspection['time_in'].replace(' : ', '').strip(), ignoretz=True))
			inspection['time_out'] = eastern.localize(parse(inspection['time_out'].replace(' : ', '').strip(), ignoretz=True))

			# Do that trick where we unpack a dict to kwargs.
			# Oooh, fancy.
			i = Inspection(**inspection)

			# If there is exactly one, set the inspection.restaurant to a get query.
			if Restaurant.objects.filter(permit_id=restaurant_id, title=restaurant_title) == 1:
				i.restaurant = Restaurant.objects.get(permit_id=restaurant_id, title=restaurant_title)

			# If there are two or more ...
			# First, set the restaurant to the first one in the query.
			if Restaurant.objects.filter(permit_id=restaurant_id, title=restaurant_title) > 1:
				i.restaurant = Restaurant.objects.filter(permit_id=restaurant_id, title=restaurant_title)[0]

				# Then, kill the dupes.
				for restaurant in Restaurant.objects.filter(permit_id=restaurant_id, title=restaurant_title)[1:]:
					restaurant.delete()

			i.save()
			print '\t+ %s' % i

			# Now it's time to save the observations.
			# Aren't you glad we saved that list?
			for observation in observations:
				o = Observation(**observation)
				o.inspection = i
				o.save()
				print '\t\t+ %s' % o

	def handle(self, *args, **options):
		"""
		Invoked when the management command is run.
		"""
		self.clear_old_data()
		self.read_json()
		self.insert_inspections()
