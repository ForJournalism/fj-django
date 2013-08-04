from django import forms
from haystack.forms import FacetedSearchForm

class RestaurantFacetedSearchForm(FacetedSearchForm):
    def __name__(self):
        return "RestaurantFacetedSearchForm"

    selected_facets = forms.CharField(required=False, widget=forms.HiddenInput)

    def search(self):
        sqs = super(RestaurantFacetedSearchForm, self).search()
        for item in self.data.getlist('selected_facets'):
            sqs = sqs.narrow(item)
        return sqs