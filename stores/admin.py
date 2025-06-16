from django.contrib import admin
from django import forms
from .models import Store, HomepageBlock, StoreHomepageBlock

class StoreHomepageBlockInline(admin.TabularInline):
    model = StoreHomepageBlock
    extra = 0
    fields = ('block_type', 'title', 'order', 'is_active')

class StoreAdminForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = '__all__'
        widgets = {
            'homepage_layout': forms.HiddenInput(),
        }

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'theme_name')
    search_fields = ('name', 'owner__username')
    list_filter = ('theme_name',)
    prepopulated_fields = {'slug': ('name',)}
    form = StoreAdminForm
    inlines = [StoreHomepageBlockInline]

@admin.register(HomepageBlock)
class HomepageBlockAdmin(admin.ModelAdmin):
    list_display = ('name', 'block_type', 'template_name')
    list_filter = ('block_type',)
    search_fields = ('name', 'description')

@admin.register(StoreHomepageBlock)
class StoreHomepageBlockAdmin(admin.ModelAdmin):
    list_display = ('store', 'block_type', 'title', 'order', 'is_active')
    list_filter = ('store', 'block_type', 'is_active')
    search_fields = ('store__name', 'title', 'content')
    list_editable = ('order', 'is_active')
    
    fieldsets = (
        (None, {
            'fields': ('store', 'block_type', 'title', 'order', 'is_active')
        }),
        ('Content', {
            'fields': ('content',),
            'classes': ('collapse',),
        }),
        ('Advanced Configuration', {
            'fields': ('configuration',),
            'classes': ('collapse',),
        }),
    )