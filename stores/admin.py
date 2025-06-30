from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from .models import Store, Product, Order, SellerProfile, ProductUploadBatch

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'subdomain', 'is_published', 'onboarding_completed', 'created_at']
    list_filter = ['is_published', 'onboarding_completed', 'theme', 'created_at']
    search_fields = ['name', 'owner__username', 'subdomain']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'owner', 'description', 'logo')
        }),
        ('Domain Settings', {
            'fields': ('subdomain', 'custom_domain')
        }),
        ('Theme & Branding', {
            'fields': ('theme', 'primary_color', 'secondary_color', 'font_family')
        }),
        ('Payment & Business', {
            'fields': ('razorpay_key_id', 'razorpay_key_secret', 'gst_number', 'business_address')
        }),
        ('Status', {
            'fields': ('onboarding_completed', 'is_published')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(SellerProfile)
class SellerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'language_preference', 'is_partner_admin', 'created_at']
    list_filter = ['language_preference', 'is_partner_admin', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']
    filter_horizontal = ['managed_stores']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Partner admins can only see their managed sellers
        if hasattr(request.user, 'sellerprofile') and request.user.sellerprofile.is_partner_admin:
            managed_store_owners = []
            for store in request.user.sellerprofile.managed_stores.all():
                managed_store_owners.append(store.owner.id)
            return qs.filter(user__id__in=managed_store_owners)
        return qs.filter(user=request.user)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'store', 'price', 'stock', 'category', 'is_active', 'created_at']
    list_filter = ['is_active', 'category', 'store', 'created_at']
    search_fields = ['name', 'description', 'store__name']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('store', 'name', 'slug', 'description', 'short_description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock', 'category')
        }),
        ('Media', {
            'fields': ('image', 'image_url')
        }),
        ('AI Enhancement', {
            'fields': ('material', 'region', 'style', 'ai_generated_description'),
            'description': 'These fields help generate better AI descriptions'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter by user's stores
        return qs.filter(store__owner=request.user)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'store', 'customer_name', 'product', 'total_amount', 'status', 'whatsapp_sent', 'created_at']
    list_filter = ['status', 'whatsapp_sent', 'store', 'created_at']
    search_fields = ['order_id', 'customer_name', 'customer_email', 'product__name']
    readonly_fields = ['order_id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_id', 'store', 'product', 'quantity', 'total_amount', 'gst_amount')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'customer_email', 'customer_phone', 'customer_address')
        }),
        ('Payment', {
            'fields': ('razorpay_order_id', 'razorpay_payment_id')
        }),
        ('Status & Notifications', {
            'fields': ('status', 'whatsapp_sent')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    actions = ['send_whatsapp_notification', 'mark_as_delivered']
    
    def send_whatsapp_notification(self, request, queryset):
        from .tasks import send_whatsapp_notification
        for order in queryset:
            send_whatsapp_notification.delay(order.id, 'status_update')
        self.message_user(request, f"WhatsApp notifications sent for {queryset.count()} orders.")
    send_whatsapp_notification.short_description = "Send WhatsApp notifications"
    
    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
        self.message_user(request, f"{queryset.count()} orders marked as delivered.")
    mark_as_delivered.short_description = "Mark as delivered"
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        # Filter by user's stores
        return qs.filter(store__owner=request.user)

@admin.register(ProductUploadBatch)
class ProductUploadBatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'store', 'total_rows', 'successful_imports', 'failed_imports', 'status', 'created_at']
    list_filter = ['status', 'store', 'created_at']
    readonly_fields = ['total_rows', 'successful_imports', 'failed_imports', 'errors', 'created_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(store__owner=request.user)

# Extend User admin to show roles
class UserInline(admin.StackedInline):
    model = SellerProfile
    can_delete = False
    verbose_name_plural = 'Profile'

class UserAdmin(BaseUserAdmin):
    inlines = (UserInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role')
    
    def get_role(self, obj):
        if obj.is_superuser:
            return '🔧 Super Admin'
        elif obj.is_staff:
            return '⚙️ Staff'
        elif hasattr(obj, 'sellerprofile'):
            if obj.sellerprofile.is_partner_admin:
                return '🏢 NGO Admin'
            else:
                return '🏪 Store Owner'
        else:
            return '👤 Customer'
    get_role.short_description = 'Role'

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)