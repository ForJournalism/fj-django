from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.template.defaultfilters import slugify
from geopy import geocoders
from geopy.geocoders.googlev3 import GQueryError, GTooManyQueriesError
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^django\.contrib\.gis"])

class Restaurant(models.Model):
	"""
	Defines a single restaurant.
	From the data source.
		u'title'
	 	u'permit_id'
	 	u'quadrant'
	 	u'address'
	 	u'ward'
	 	u'type'
	 	u'inspection_url'
	"""
	title = models.CharField(max_length=255, db_index=True)
	permit_id = models.CharField(max_length=255)
	quadrant = models.CharField(max_length=2, db_index=True)
	address = models.TextField(null=True)
	ward = models.CharField(max_length=255, null=True)
	restaurant_type = models.CharField(max_length=255, null=True)
	inspection_url = models.TextField(null=True)
	slug = models.SlugField(max_length=255)
	inspection_count = models.IntegerField(default=0)
	observation_count = models.IntegerField(default=0)
	point = models.PointField(null=True)

	objects = models.GeoManager()

	class Meta():
		ordering = ['title']

	def __unicode__(self):
		return '%s (%s)' % (self.title, self.permit_id)

	@property
	def inspections(self):
		from inspections.inspection.models import Inspection
		return Inspection.objects.filter(restaurant=self)

	def get_observation_count(self):
		from inspections.inspection.models import Inspection, Observation
		observation_count = 0
		for inspection in Inspection.objects.filter(restaurant=self):
			observation_count += len(inspection.observation_set.all())
		return observation_count

	def get_inspection_count(self):
		from inspections.inspection.models import Inspection
		return Inspection.objects.filter(restaurant=self).count()

	def admin_point(self):
		if self.point:
			return '%s, %s' % (self.point.y, self.point.x)
		return None

	def save(self, *args, **kwargs):
		"""
		Override the save method to handle some preprocessing.
		"""
		if not self.point:
			g = geocoders.GoogleV3()

			try:
				place, (lat, lng) = g.geocode(self.address)
				self.point = Point(lng, lat)

			except ValueError:
				pass

			except GQueryError:
				pass

			except GTooManyQueriesError:
				pass



		# Create the slug if it doesn't exist.
		# Don't overwrite the slug if it does.
		# Cool URLs don't change.
		if not self.slug:
			self.slug = slugify('%s %s' % (self.title, self.permit_id))

		self.inspection_count = self.get_inspection_count()
		self.observation_count = self.get_observation_count()
		
		super(Restaurant, self).save(**kwargs)