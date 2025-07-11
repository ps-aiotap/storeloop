from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from ...models import Lead, Interaction
from ...langchain_pipeline import crm_ai
from ...context.context_protocol import FollowUpContext, ConversationContext
from ...utils.mode_context import get_crm_mode

class Command(BaseCommand):
    help = 'Generate AI-powered follow-up recommendations for stale leads'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Days since last contact to trigger follow-up'
        )
        parser.add_argument(
            '--limit',
            type=int,
            default=50,
            help='Maximum number of leads to process'
        )
    
    def handle(self, *args, **options):
        days_threshold = options['days']
        limit = options['limit']
        
        cutoff_date = timezone.now() - timedelta(days=days_threshold)
        
        # Find leads with no recent interactions
        stale_leads = Lead.objects.using('crm_db').filter(
            customer__interactions__created_at__lt=cutoff_date
        ).distinct()[:limit]
        
        self.stdout.write(f"Processing {stale_leads.count()} stale leads...")
        
        processed = 0
        for lead in stale_leads:
            try:
                # Get customer interaction history
                interactions = lead.customer.interactions.using('crm_db').order_by('-created_at')[:5]
                interaction_history = [f"{i.direction}: {i.content}" for i in interactions]
                
                # Get customer tags
                tags = [ct.tag.name for ct in lead.customer.customertag_set.using('crm_db').select_related('tag')]
                
                # Calculate days since last contact
                last_interaction = interactions.first()
                days_since_contact = (timezone.now() - last_interaction.created_at).days if last_interaction else 30
                
                # Build context
                conversation_context = ConversationContext(
                    customer_name=lead.customer.name,
                    interaction_history=interaction_history,
                    last_contact_date=last_interaction.created_at if last_interaction else timezone.now(),
                    tags=tags,
                    channel=last_interaction.channel if last_interaction else 'email',
                    mode=get_crm_mode().lower()
                )
                
                followup_context = FollowUpContext(
                    customer_context=conversation_context,
                    days_since_contact=days_since_contact,
                    previous_followups=[]  # Could track this in future
                )
                
                # Generate AI follow-up recommendation
                followup_suggestion = crm_ai.recommend_followup(followup_context)
                
                # Update lead with AI recommendation
                lead.ai_next_action = followup_suggestion
                lead.next_followup = timezone.now() + timedelta(days=1)
                lead.save(using='crm_db')
                
                # Optionally create an interaction record
                Interaction.objects.using('crm_db').create(
                    customer=lead.customer,
                    channel='internal',
                    direction='internal',
                    content=f"AI Follow-up Suggestion: {followup_suggestion}",
                    summary="AI-generated follow-up recommendation"
                )
                
                processed += 1
                self.stdout.write(f"✓ Generated follow-up for {lead.customer.name}")
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"✗ Failed to process {lead.customer.name}: {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {processed} leads")
        )