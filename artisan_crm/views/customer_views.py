from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from datetime import datetime

from ..models import CustomerProfile, Interaction, Lead, Tag
from ..utils.mode_context import ModeContextMixin, get_crm_mode, get_mode_config
from ..langchain_pipeline import crm_ai
from ..context.context_protocol import ConversationContext, ReplyContext

class CustomerListView(LoginRequiredMixin, ModeContextMixin, ListView):
    model = CustomerProfile
    template_name = 'artisan_crm/customer_list.html'
    context_object_name = 'customers'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = CustomerProfile.objects.using('crm_db').select_related().prefetch_related('interactions')
        
        # Filter by search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        
        # Filter by tags
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(customertag__tag__name=tag)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.using('crm_db').all()
        context['search'] = self.request.GET.get('search', '')
        context['selected_tag'] = self.request.GET.get('tag', '')
        return context

class CustomerDetailView(LoginRequiredMixin, ModeContextMixin, DetailView):
    model = CustomerProfile
    template_name = 'artisan_crm/customer_detail.html'
    context_object_name = 'customer'
    
    def get_object(self):
        return get_object_or_404(CustomerProfile.objects.using('crm_db'), pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = self.get_object()
        
        # Get interactions timeline
        interactions = customer.interactions.using('crm_db').order_by('-created_at')[:20]
        context['interactions'] = interactions
        
        # Get lead info if exists
        try:
            lead = Lead.objects.using('crm_db').get(customer=customer)
            context['lead'] = lead
        except Lead.DoesNotExist:
            context['lead'] = None
        
        # Get customer tags
        context['customer_tags'] = [ct.tag for ct in customer.customertag_set.using('crm_db').select_related('tag')]
        
        return context

@csrf_exempt
def generate_summary(request, customer_id):
    """Generate AI summary for customer"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    customer = get_object_or_404(CustomerProfile.objects.using('crm_db'), pk=customer_id)
    
    # Build conversation context
    interactions = customer.interactions.using('crm_db').order_by('-created_at')[:10]
    interaction_history = [f"{i.direction}: {i.content}" for i in interactions]
    
    tags = [ct.tag.name for ct in customer.customertag_set.using('crm_db').select_related('tag')]
    
    context = ConversationContext(
        customer_name=customer.name,
        interaction_history=interaction_history,
        last_contact_date=interactions[0].created_at if interactions else datetime.now(),
        tags=tags,
        channel=interactions[0].channel if interactions else 'email',
        mode=get_crm_mode().lower()
    )
    
    # Generate summary
    summary = crm_ai.summarize_conversation(context)
    
    # Update customer summary
    customer.summary = summary
    customer.save(using='crm_db')
    
    return JsonResponse({'summary': summary})

@csrf_exempt
def suggest_reply(request, customer_id):
    """Generate AI reply suggestion"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    data = json.loads(request.body)
    message_text = data.get('message', '')
    
    customer = get_object_or_404(CustomerProfile.objects.using('crm_db'), pk=customer_id)
    
    # Build contexts
    interactions = customer.interactions.using('crm_db').order_by('-created_at')[:5]
    interaction_history = [f"{i.direction}: {i.content}" for i in interactions]
    tags = [ct.tag.name for ct in customer.customertag_set.using('crm_db').select_related('tag')]
    
    conversation_context = ConversationContext(
        customer_name=customer.name,
        interaction_history=interaction_history,
        last_contact_date=interactions[0].created_at if interactions else datetime.now(),
        tags=tags,
        channel=interactions[0].channel if interactions else 'email',
        mode=get_crm_mode().lower()
    )
    
    reply_context = ReplyContext(
        message_text=message_text,
        customer_context=conversation_context
    )
    
    # Generate reply
    suggested_reply = crm_ai.suggest_reply(reply_context)
    
    return JsonResponse({'reply': suggested_reply})

@csrf_exempt
def add_interaction(request, customer_id):
    """Add new interaction"""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    data = json.loads(request.body)
    customer = get_object_or_404(CustomerProfile.objects.using('crm_db'), pk=customer_id)
    
    interaction = Interaction.objects.using('crm_db').create(
        customer=customer,
        channel=data.get('channel', 'internal'),
        direction=data.get('direction', 'outbound'),
        content=data.get('content', '')
    )
    
    return JsonResponse({
        'id': interaction.id,
        'content': interaction.content,
        'channel': interaction.channel,
        'direction': interaction.direction,
        'created_at': interaction.created_at.isoformat()
    })