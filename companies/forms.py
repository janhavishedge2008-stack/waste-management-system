from django import forms
from .models import CompanyWasteRequest

class CompanyWasteRequestForm(forms.ModelForm):
    class Meta:
        model = CompanyWasteRequest
        fields = ['waste_type', 'quantity', 'unit', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
