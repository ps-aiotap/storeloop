from django import forms
from .models import Store

class StoreThemeForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['theme_name', 'primary_color', 'font_choice', 'logo', 'custom_css', 'custom_js', 'theme_version']
        widgets = {
            'custom_css': forms.Textarea(attrs={'rows': 10, 'class': 'font-mono text-sm'}),
            'custom_js': forms.Textarea(attrs={'rows': 10, 'class': 'font-mono text-sm'}),
        }
        
    def clean_custom_css(self):
        css = self.cleaned_data.get('custom_css')
        # Basic validation to prevent XSS
        if css and ('<script' in css.lower() or 'javascript:' in css.lower()):
            raise forms.ValidationError("Custom CSS cannot contain script tags or JavaScript")
        return css
        
    def clean_custom_js(self):
        js = self.cleaned_data.get('custom_js')
        # Basic validation - could be enhanced with a JS validator library
        return js