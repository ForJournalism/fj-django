from django.views.generic import DetailView

from inspections.inspection.models import Inspection

class InspectionDetail(DetailView):
	model = Inspection
	queryset = Inspection.objects.all()