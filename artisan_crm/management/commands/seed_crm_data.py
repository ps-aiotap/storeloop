from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from ...models import CustomerProfile, Tag, LeadStage, Lead, Interaction
from ...integrations.mock_channels import mock_connector
from ...utils.mode_context import get_crm_mode, get_mode_config

class Command(BaseCommand):
    help = 'Seed CRM with sample data based on current mode'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--customers',
            type=int,
            default=10,
            help='Number of customers to create'
        )
    
    def handle(self, *args, **options):
        customer_count = options['customers']
        mode = get_crm_mode().lower()
        config = get_mode_config()
        
        self.stdout.write(f"Seeding CRM data for {mode.upper()} mode...")
        
        # Create tags
        self._create_tags(config['default_tags'])
        
        # Create lead stages
        self._create_lead_stages(config['lead_stages'], mode)
        
        # Create customers with interactions
        self._create_customers(customer_count, mode)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully seeded {customer_count} customers"))
    
    def _create_tags(self, tag_names):
        colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6', '#06B6D4']
        
        for i, tag_name in enumerate(tag_names):
            tag, created = Tag.objects.using('crm_db').get_or_create(
                name=tag_name,
                defaults={
                    'color': colors[i % len(colors)],
                    'description': f'Auto-generated tag for {tag_name}'
                }
            )
            if created:
                self.stdout.write(f"Created tag: {tag_name}")
    
    def _create_lead_stages(self, stage_names, mode):
        colors = ['#6B7280', '#3B82F6', '#F59E0B', '#10B981', '#EF4444', '#8B5CF6']
        
        for i, stage_name in enumerate(stage_names):
            stage, created = LeadStage.objects.using('crm_db').get_or_create(
                name=stage_name,
                mode=mode,
                defaults={
                    'order': i,
                    'color': colors[i % len(colors)]
                }
            )
            if created:
                self.stdout.write(f"Created stage: {stage_name}")
    
    def _create_customers(self, count, mode):
        if mode == 'storeloop':
            customer_data = self._get_storeloop_customers()
        else:
            customer_data = self._get_aiotap_customers()
        
        tags = list(Tag.objects.using('crm_db').all())
        stages = list(LeadStage.objects.using('crm_db').filter(mode__in=[mode, 'shared']))
        
        for i in range(count):
            data = random.choice(customer_data)
            
            # Create customer
            customer = CustomerProfile.objects.using('crm_db').create(
                name=data['name'],
                email=data['email'],
                phone=data.get('phone', ''),
                company=data.get('company', ''),
                source=random.choice(['whatsapp', 'email', 'referral', 'manual']),
                created_at=timezone.now() - timedelta(days=random.randint(1, 90))
            )
            
            # Add random tags
            selected_tags = random.sample(tags, random.randint(1, 3))
            for tag in selected_tags:
                from ...models import CustomerTag
                CustomerTag.objects.using('crm_db').create(customer=customer, tag=tag)
            
            # Create lead
            lead = Lead.objects.using('crm_db').create(
                customer=customer,
                stage=random.choice(stages),
                score=random.randint(1, 100),
                next_followup=timezone.now() + timedelta(days=random.randint(1, 14))
            )
            
            # Generate mock interactions
            interactions = mock_connector.generate_mock_interactions(customer, random.randint(2, 8))
            for interaction in interactions:
                interaction.save(using='crm_db')
            
            self.stdout.write(f"Created customer: {customer.name}")
    
    def _get_storeloop_customers(self):
        return [
            {'name': 'Priya Sharma', 'email': 'priya.sharma@gmail.com', 'phone': '+919876543210'},
            {'name': 'Rajesh Kumar', 'email': 'rajesh.kumar@yahoo.com', 'phone': '+919876543211'},
            {'name': 'Anita Devi', 'email': 'anita.devi@gmail.com', 'phone': '+919876543212'},
            {'name': 'Suresh Patel', 'email': 'suresh.patel@hotmail.com', 'phone': '+919876543213'},
            {'name': 'Meera Gupta', 'email': 'meera.gupta@gmail.com', 'phone': '+919876543214'},
            {'name': 'Vikram Singh', 'email': 'vikram.singh@gmail.com', 'phone': '+919876543215'},
            {'name': 'Kavita Joshi', 'email': 'kavita.joshi@yahoo.com', 'phone': '+919876543216'},
            {'name': 'Amit Verma', 'email': 'amit.verma@gmail.com', 'phone': '+919876543217'},
            {'name': 'Sunita Rao', 'email': 'sunita.rao@hotmail.com', 'phone': '+919876543218'},
            {'name': 'Deepak Agarwal', 'email': 'deepak.agarwal@gmail.com', 'phone': '+919876543219'},
        ]
    
    def _get_aiotap_customers(self):
        return [
            {'name': 'Sarah Johnson', 'email': 'sarah@techstartup.com', 'company': 'TechStartup Inc'},
            {'name': 'Michael Chen', 'email': 'michael@innovate.co', 'company': 'Innovate Solutions'},
            {'name': 'Emily Rodriguez', 'email': 'emily@datadriven.io', 'company': 'DataDriven Analytics'},
            {'name': 'David Kim', 'email': 'david@aiventures.com', 'company': 'AI Ventures'},
            {'name': 'Lisa Thompson', 'email': 'lisa@smarttech.org', 'company': 'SmartTech Solutions'},
            {'name': 'James Wilson', 'email': 'james@futureai.net', 'company': 'Future AI Labs'},
            {'name': 'Anna Kowalski', 'email': 'anna@mlstartup.com', 'company': 'ML Startup'},
            {'name': 'Robert Taylor', 'email': 'robert@techcorp.biz', 'company': 'TechCorp International'},
            {'name': 'Maria Garcia', 'email': 'maria@aicompany.co', 'company': 'AI Company Ltd'},
            {'name': 'John Anderson', 'email': 'john@innovation.tech', 'company': 'Innovation Tech'},
        ]