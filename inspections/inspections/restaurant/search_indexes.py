from haystack import indexes
from inspections.restaurant.models import Restaurant


class RestaurantIndex(indexes.SearchIndex, indexes.Indexable):
	# For keyword searches.
    text = indexes.CharField(document=True, use_template=True)

    # For building out search results.
    title = indexes.CharField(model_attr="title")
    address = indexes.CharField(model_attr="address")
    quadrant = indexes.CharField(model_attr="quadrant", faceted=True)
    inspection_count = indexes.CharField(model_attr="inspection_count")
    observation_count = indexes.CharField(model_attr="observation_count")

    def get_model(self):
        return Restaurant

    def index_queryset(self, using=None):
        return self.get_model().objects.all()