from django import forms
from .models import Listing

class listingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid','image_url','category']



class commentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control", "rows":"3", "placeholder":"Add Comment"}))



class bidsForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)