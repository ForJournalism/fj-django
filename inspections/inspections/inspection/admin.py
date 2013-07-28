from django.contrib import admin
from inspections.inspection.models import Inspection
from inspections.inspection.models import Observation

class InspectionInline(admin.TabularInline):
	model = Inspection
	extra = 0
	fields = ('time_in', 'time_out', 'critical', 'critical_corrected_on_site', 'noncritical', 'noncritical_corrected_on_site')
	readonly_fields = fields

class ObservationInline(admin.TabularInline):
	model = Observation
	extra = 0
	fields = ('dcmr', 'observation', 'correction')
	readonly_fields = fields

class InspectionAdmin(admin.ModelAdmin):
	inlines = [ ObservationInline ]
	list_display = ('restaurant', 'inspection_id', 'time_in', 'critical', 'noncritical')
	readonly_fields = ('restaurant', 'time_in', 'time_out',)
	fieldsets = (
		(None, {
			'fields': (('inspection_type', 'risk_category'), 'restaurant')
		}),
		('Date', {
			'fields': (('time_in', 'time_out'),)
		}),
		('Violations', {
			'fields': (('critical', 'critical_corrected_on_site'), ('noncritical', 'noncritical_corrected_on_site'))
		}),
		('Advanced options', {
			'classes': ('collapse',),
			'fields': ('inspection_id', 'inspection_url')
		}),
	)

admin.site.register(Inspection, InspectionAdmin)
# admin.site.register(Observation)