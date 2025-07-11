from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
import json

from ..models import Lead, LeadStage, CustomerProfile
from ..utils.mode_context import ModeContextMixin, filter_by_mode

class LeadPipelineView(LoginRequiredMixin, ModeContextMixin, TemplateView):
    template_name = 'artisan_crm/lead_pipeline.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get stages for current mode
        stages = filter_by_mode(LeadStage.objects.using('crm_db')).filter(is_active=True)
        
        # Get leads grouped by stage
        pipeline_data = []
        for stage in stages:
            leads = Lead.objects.using('crm_db').filter(stage=stage).select_related('customer')
            pipeline_data.append({
                'stage': stage,
                'leads': leads,
                'count': leads.count()
            })
        
        context['pipeline_data'] = pipeline_data
        context['total_leads'] = Lead.objects.using('crm_db').count()
        
        return context

@csrf_exempt
def move_lead(request):
    """Move lead to different stage via HTMX"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    data = json.loads(request.body)
    lead_id = data.get('lead_id')
    new_stage_id = data.get('stage_id')
    
    try:
        lead = Lead.objects.using('crm_db').get(id=lead_id)
        new_stage = LeadStage.objects.using('crm_db').get(id=new_stage_id)
        
        lead.stage = new_stage
        lead.save(using='crm_db')
        
        return JsonResponse({
            'success': True,
            'lead_id': lead.id,
            'customer_name': lead.customer.name,
            'new_stage': new_stage.name
        })
    
    except (Lead.DoesNotExist, LeadStage.DoesNotExist):
        return JsonResponse({'error': 'Lead or stage not found'}, status=404)