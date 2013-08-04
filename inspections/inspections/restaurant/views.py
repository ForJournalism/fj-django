from django.contrib.gis.measure import D
from django.views.generic import ListView, DetailView

from inspections.restaurant.models import Restaurant
from inspections.inspection.models import Inspection

def restaurant_list_context():
	"""
	A generic function for building context for restaurant list pages.
	Or, really, any page that wants details about restaurants.
	"""
	context = {}
	restaurants = Restaurant.objects.all()
	context['top_10_inspections'] = restaurants.order_by('-inspection_count').values('title', 'inspection_count', 'id')[:10]
	context['top_10_violations'] = restaurants.order_by('-observation_count').values('title', 'inspection_count', 'id')[:10]
	context['recent_10_inspections'] = Inspection.objects.all().order_by('-time_in').values('restaurant__title', 'time_in', 'restaurant__id')[:10]

	context['quadrants'] = []
	for quadrant in ['NE', 'NW', 'SE', 'SW']:
		quadrant_dict = {}
		quadrant_dict['name'] = quadrant
		quadrant_dict['restaurant_count'] = Restaurant.objects.filter(quadrant=quadrant).count()
		context['quadrants'].append(quadrant_dict)

	return context


class RestaurantByQuadrantList(ListView):
	"""
	Returns a list of restaurants by quadrant.
	"""
	model = Restaurant

	def get_queryset(self):
		"""
		Limit the queryset to a single quadrant.
		"""
		self.quadrant = self.args[0]
		return Restaurant.objects.filter(quadrant=self.quadrant)

	def get_context_data(self, **kwargs):
		"""
		Build the charts.
		"""
		context = super(RestaurantByQuadrantList, self).get_context_data(**kwargs)
		context = dict(context, **restaurant_list_context())
		context['page_title'] = '%s restaurants' % self.quadrant
		return context

class RestaurantList(ListView):
	"""
	Returns all restaurants.
	"""
	model = Restaurant

	def get_context_data(self, **kwargs):
		"""
		Build the charts.
		"""
		context = super(RestaurantList, self).get_context_data(**kwargs)
		context = dict(context, **restaurant_list_context())
		context['page_title'] = 'All restaurants'
		return context

class RestaurantDetail(DetailView):
	"""
	Return a single restaurant.
	"""
	model = Restaurant
	queryset = Restaurant.objects.all()

	def get_context_data(self, **kwargs):
		context = super(RestaurantDetail, self).get_context_data(**kwargs)
		restaurant = super(RestaurantDetail, self).get_object()
		context['nearby_restaurants'] = Restaurant.objects\
											.filter(point__distance_lte=(restaurant.point, D(ft=1000)))\
											.filter(point__distance_gt=(restaurant.point, D(ft=0)))\
											.distance(restaurant.point)\
											.values('title', 'id', 'distance')\
											.order_by('distance')
		return context
