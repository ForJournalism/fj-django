from django.conf.urls import patterns, include, url
from django.contrib import admin
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from inspections.inspection.views import InspectionDetail
from inspections.restaurant.forms import RestaurantFacetedSearchForm
from inspections.restaurant.models import Restaurant
from inspections.restaurant.views import RestaurantList, RestaurantDetail, RestaurantByQuadrantList
from inspections.restaurant.api.v1 import RestaurantResource

admin.autodiscover()
restaurant_v1 = RestaurantResource()

sqs = SearchQuerySet().facet('quadrant')

urlpatterns = patterns('',
    url(r'^inspection/(?P<pk>\d+)/$', InspectionDetail.as_view(), name='inspection-detail'),
    url(r'^restaurant/(?P<pk>\d+)/$', RestaurantDetail.as_view(), name='restaurant-detail'),
    url(r'^restaurants/([\w-]+)/$', RestaurantByQuadrantList.as_view(), name='restaurant-by-quadrant'),
    url(r'^restaurants/$', RestaurantList.as_view(), name='all-restaurants'),
    url(r'^api/v1/', include(restaurant_v1.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^search/', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='restaurant-search'),
)

