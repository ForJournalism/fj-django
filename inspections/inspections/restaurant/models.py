from django.db import models
from django.template.defaultfilters import slugify

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
	title = models.CharField(max_length=255)
	permit_id = models.CharField(max_length=255)
	quadrant = models.CharField(max_length=2, null=True)
	address = models.TextField(null=True)
	ward = models.CharField(max_length=255, null=True)
	restaurant_type = models.CharField(max_length=255, null=True)
	inspection_url = models.TextField(null=True)
	slug = models.SlugField(max_length=255)

	def __unicode__(self):
		return self.title

	def save(self):
		"""
		Override the save method to handle some preprocessing.
		"""

		# Create the slug if it doesn't exist.
		# Don't overwrite the slug if it does.
		# Cool URLs don't change.
		if not self.slug:
			self.slug = slugify('%s %s' % (self.title, self.permit_id))
		
		super(Restaurant, self).save(**kwargs)