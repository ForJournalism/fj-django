from django.conf.urls import patterns, include, url
from django.contrib import admin

from inspections.inspection.views import InspectionDetail
from inspections.restaurant.views import RestaurantList, RestaurantDetail

admin.autodiscover()

urlpatterns = patterns('',
	url(r'^inspections/(?P<pk>\d+)/$', InspectionDetail.as_view(), name='inspection-detail'),
	url(r'^restaurants/(?P<pk>\d+)/$', RestaurantDetail.as_view(), name='restaurant-detail'),
	url(r'^restaurants/$', RestaurantList.as_view()),
	url(r'^admin/', include(admin.site.urls)),
)
