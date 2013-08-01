from django.conf.urls import patterns, include, url
from django.contrib import admin

from inspections.inspection.views import InspectionDetail
from inspections.restaurant.views import RestaurantList, RestaurantDetail, RestaurantByQuadrantList

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^inspection/(?P<pk>\d+)/$', InspectionDetail.as_view(), name='inspection-detail'),
	url(r'^restaurant/(?P<pk>\d+)/$', RestaurantDetail.as_view(), name='restaurant-detail'),
	url(r'^restaurants/([\w-]+)/$', RestaurantByQuadrantList.as_view(), name='restaurant-by-quadrant'),
	url(r'^restaurants/$', RestaurantList.as_view(), name='all-restaurants'),
	url(r'^admin/', include(admin.site.urls)),
)
