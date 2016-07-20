from django import forms
from .models import Gem


class GemsForm(forms.ModelForm):
    class Meta:
        model = Gem
        fields = '__all__'

