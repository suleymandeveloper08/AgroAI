from django import forms
from .models import PlantDiagnosis

class PlantUploadForm(forms.ModelForm):
    class Meta:
        model = PlantDiagnosis
        fields = ['plant_type', 'image']