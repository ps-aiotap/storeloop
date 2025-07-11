from django.contrib import admin
from .models import CustomerProfile, Tag, LeadStage, Interaction, Campaign, Lead
from .utils.mode_context import get_crm_mode, filter_by_mode

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'source', 'created_at']
    list_filter = ['source', 'created_at']
    search_fields = ['name', 'email', 'phone']
    readonly_fields = ['summary', 'intent_classification']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'description']
    
@admin.register(LeadStage)
class LeadStageAdmin(admin.ModelAdmin):
    list_display = ['name', 'mode', 'order', 'is_active']
    list_filter = ['mode', 'is_active']
    ordering = ['order']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return filter_by_mode(qs)

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ['customer', 'channel', 'direction', 'created_at']
    list_filter = ['channel', 'direction', 'created_at']
    readonly_fields = ['summary', 'intent', 'sentiment']

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'sent_count', 'created_at']
    list_filter = ['is_active', 'created_at']

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['customer', 'stage', 'score', 'next_followup']
    list_filter = ['stage', 'created_at']