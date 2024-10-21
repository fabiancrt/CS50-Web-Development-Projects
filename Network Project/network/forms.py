from django import forms
from .models import Profile

#necessary form for the profile picture function i implemented

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture']