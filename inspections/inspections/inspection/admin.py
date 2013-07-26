from django.contrib import admin
from inspections.inspection.models import Inspection
from inspections.inspection.models import Observation

admin.site.register(Inspection)
admin.site.register(Observation)