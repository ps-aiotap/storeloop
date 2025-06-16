from django import forms
from .models import Store

class StoreThemeForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = [
            'theme_name', 
            'theme_version', 
            'primary_color', 
            'font_choice', 
            'logo_url',  # This matches the field name in the model
            'custom_css', 
            'custom_js'
        ]
        widgets = {
            'primary_color': forms.TextInput(attrs={'type': 'color'}),
            'custom_css': forms.Textarea(attrs={'rows': 6}),
            'custom_js': forms.Textarea(attrs={'rows': 6}),
        }

    class Media:
        css = {
            'all': ('css/theme-editor.css',)
        }
        js = ('js/theme-editor.js',)