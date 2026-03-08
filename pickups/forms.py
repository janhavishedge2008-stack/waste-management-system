from django import forms
from .models import PickupRequest

class PickupRequestForm(forms.ModelForm):
    class Meta:
        model = PickupRequest
        fields = ['waste_type', 'location', 'pickup_date', 'pickup_time', 'quantity_estimate', 'special_instructions']
        widgets = {
            'pickup_date': forms.DateInput(attrs={'type': 'date'}),
            'pickup_time': forms.TimeInput(attrs={'type': 'time'}),
            'special_instructions': forms.Textarea(attrs={'rows': 3}),
        }
