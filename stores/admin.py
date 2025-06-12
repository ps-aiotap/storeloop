from django.contrib import admin
from .models import Store

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'theme_name', 'primary_color', 'font_choice')
    list_filter = ('theme_name', 'font_choice')
    search_fields = ('name', 'owner__username')