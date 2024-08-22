from django import forms
from .models import Destination

class DestinationForm(forms.ModelForm):
    class Meta:
        model = Destination
        fields = '__all__'
        widgets = {
            'place_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter place name'}),
            'weather': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter weather'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter location'}),
            'google_map_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter Google Map link'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description'}),
        }
