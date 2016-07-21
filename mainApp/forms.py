from django import forms
from .models import Gem, Category


class GemsForm(forms.ModelForm):
    class Meta:
        model = Gem
        fields = '__all__'


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'