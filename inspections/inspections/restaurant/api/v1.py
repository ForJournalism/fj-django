from tastypie import fields
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from inspections.restaurant.models import Restaurant
from inspections.inspection.models import Inspection, Observation


class RestaurantResource(ModelResource):
	inspections = fields.CharField(null=True)
	point = fields.CharField(null=True)

	class Meta:
		queryset = Restaurant.objects.all()
		resource_name = 'restaurant'
		allowed_methods = ['get']
		filtering = {
			'title': ALL,
			'anc': ALL, 
			'quadrant': ALL,
			'inspection_count': ALL,
			'observation_count': ALL
		}

	def dehydrate_point(self, bundle):
		"""
		Build out the point field.
		"""
		if bundle.obj.point:

			# Eval this into a dictionary, which it is.
			return eval(bundle.obj.point.geojson)

		return None

	def dehydrate_inspections(self, bundle):
		"""
		Build the API output for a restaurant.
		"""
		inspections = {}

		# Wouldn't it be nice to get a count?
		inspections['objects'] = []

		for i in Inspection.objects.filter(restaurant=bundle.obj):

			# Get a dictionary representation of this object.
			inspection_dict = i.__dict__
			inspection_dict.pop('_state')

			# Loop over the related observations and return those too.
			inspection_dict['observations'] = {}
			inspection_dict['observations']['count'] = Observation.objects.filter(inspection=i).count()
			inspection_dict['observations']['objects'] = []

			# Get the actual observations.
			for o in Observation.objects.filter(inspection=i).values('observation', 'dcmr', 'correction'):
				inspection_dict['observations']['objects'].append(o)

			# Attache the inspection object
			inspections['objects'].append(inspection_dict)

		return inspections
