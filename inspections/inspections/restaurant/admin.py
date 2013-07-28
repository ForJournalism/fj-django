from django.contrib import admin
from inspections.restaurant.models import Restaurant
from inspections.inspection.admin import InspectionInline

class RestaurantAdmin(admin.ModelAdmin):
	inlines = [ InspectionInline ]
	list_display = ('title', 'quadrant', 'inspection_count')
	readonly_fields = ('address', 'quadrant', 'ward', 'title', 'permit_id')
	fieldsets = (
		(None, {
			'fields': (('title', 'permit_id', 'restaurant_type'),)
		}),
		('Location', {
			'fields': (('quadrant', 'ward', 'address'),)
		}),
		('Advanced options', {
			'classes': ('collapse',),
			'fields': ('inspection_url', 'slug')
		}),
	)

admin.site.register(Restaurant, RestaurantAdmin)