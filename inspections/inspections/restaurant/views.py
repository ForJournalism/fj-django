from django.contrib.gis.measure import D
from django.views.generic import ListView, DetailView

from inspections.restaurant.models import Restaurant

class RestaurantList(ListView):
    model = Restaurant

class RestaurantDetail(DetailView):
	model = Restaurant
	queryset = Restaurant.objects.all()

	def get_context_data(self, **kwargs):
		context = super(RestaurantDetail, self).get_context_data(**kwargs)
		restaurant = super(RestaurantDetail, self).get_object()
		context['nearby_restaurants'] = Restaurant.objects\
											.filter(point__distance_lte=(restaurant.point, D(ft=1000)))\
											.filter(point__distance_gt=(restaurant.point, D(ft=0)))\
											.distance(restaurant.point)\
											.order_by('distance')
		return context
