from django import forms
from .models import Listing

class CreateListingForm(forms.Form):
    class Meta: 
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows':4}),
        }