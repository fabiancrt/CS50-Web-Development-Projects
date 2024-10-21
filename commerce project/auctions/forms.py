from django import forms
from .models import ProductListing, Offer, Review

#here are the required forms , basic forms , nothing to special here also

class AddProductForm(forms.ModelForm):
    class Meta:
        model = ProductListing
        fields = ['name', 'details', 'initial_price', 'image_link', 'category_name']

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['offer_price']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text']