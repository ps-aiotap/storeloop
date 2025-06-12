from django import forms
from .models import Store

class StoreThemeForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['theme_name', 'primary_color', 'font_choice', 'logo']
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
        }