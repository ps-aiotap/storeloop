from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CustomerProfile(models.Model):
    # Store user ID instead of foreign key to avoid cross-database issues
    storeloop_user_id = models.IntegerField(null=True, blank=True, help_text="Reference to StoreLoop User ID")
    
    # Core customer data
    name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    whatsapp_number = models.CharField(max_length=20, blank=True)
    
    # Business context
    company = models.CharField(max_length=200, blank=True)
    role = models.CharField(max_length=100, blank=True)
    
    # CRM metadata
    source = models.CharField(max_length=50, choices=[
        ('storeloop_order', 'StoreLoop Order'),
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('upwork', 'Upwork'),
        ('referral', 'Referral'),
        ('manual', 'Manual Entry')
    ])
    
    # AI-generated fields
    summary = models.TextField(blank=True, help_text="AI-generated customer summary")
    intent_classification = models.CharField(max_length=100, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'crm_customer_profile'
    
    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#3B82F6')  # Hex color
    description = models.TextField(blank=True)
    
    class Meta:
        db_table = 'crm_tag'
    
    def __str__(self):
        return self.name

class LeadStage(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=7, default='#6B7280')
    is_active = models.BooleanField(default=True)
    
    # Mode-specific stages
    mode = models.CharField(max_length=20, choices=[
        ('storeloop', 'StoreLoop'),
        ('aiotap', 'AioTap'),
        ('shared', 'Shared')
    ], default='shared')
    
    class Meta:
        db_table = 'crm_lead_stage'
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Interaction(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, related_name='interactions')
    
    # Interaction data
    channel = models.CharField(max_length=20, choices=[
        ('whatsapp', 'WhatsApp'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('upwork', 'Upwork'),
        ('internal', 'Internal Note')
    ])
    
    direction = models.CharField(max_length=10, choices=[
        ('inbound', 'Inbound'),
        ('outbound', 'Outbound'),
        ('internal', 'Internal')
    ])
    
    content = models.TextField()
    
    # AI-generated fields
    summary = models.TextField(blank=True)
    intent = models.CharField(max_length=100, blank=True)
    sentiment = models.CharField(max_length=20, blank=True)
    
    # Metadata
    external_id = models.CharField(max_length=100, blank=True)  # WhatsApp message ID, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'crm_interaction'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.customer.name} - {self.channel} - {self.created_at.strftime('%Y-%m-%d')}"

class Campaign(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Campaign targeting
    target_tags = models.ManyToManyField(Tag, blank=True)
    target_stage = models.ForeignKey(LeadStage, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Campaign content
    message_template = models.TextField()
    
    # AI-generated variations
    ai_variations = models.JSONField(default=list, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    sent_count = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'crm_campaign'
    
    def __str__(self):
        return self.name

# Many-to-many relationship for customer tags
class CustomerTag(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'crm_customer_tag'
        unique_together = ('customer', 'tag')

# Lead pipeline tracking
class Lead(models.Model):
    customer = models.OneToOneField(CustomerProfile, on_delete=models.CASCADE)
    stage = models.ForeignKey(LeadStage, on_delete=models.CASCADE)
    
    # Lead scoring
    score = models.IntegerField(default=0)
    
    # Follow-up tracking
    next_followup = models.DateTimeField(null=True, blank=True)
    followup_count = models.PositiveIntegerField(default=0)
    
    # AI recommendations
    ai_next_action = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'crm_lead'
    
    def __str__(self):
        return f"{self.customer.name} - {self.stage.name}"