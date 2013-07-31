from django.contrib.gis import admin
from inspections.restaurant.models import Restaurant
from inspections.inspection.admin import InspectionInline

class RestaurantAdmin(admin.OSMGeoAdmin):
	inlines = [ InspectionInline ]
	list_display = ('title', 'quadrant', 'inspection_count', 'admin_point')
	readonly_fields = ('address', 'quadrant', 'ward', 'title', 'permit_id')
	search_fields = ['address', 'title']
	list_filter = ('quadrant',)
	fieldsets = (
		(None, {
			'fields': (('title', 'permit_id', 'restaurant_type'),)
		}),
		('Location', {
			'fields': (('quadrant', 'ward', 'address'), 'point')
		}),
		('Advanced options', {
			'classes': ('collapse',),
			'fields': ('inspection_url', 'slug')
		}),
	)

admin.site.register(Restaurant, RestaurantAdmin)