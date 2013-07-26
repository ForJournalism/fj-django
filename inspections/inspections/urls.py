from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'inspections.views.home', name='home'),
    # url(r'^inspections/', include('inspections.foo.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
