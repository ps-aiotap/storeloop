from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Product, 
    TagType, 
    Tag, 
    Bundle, 
    BundleItem, 
    StaticPage, 
    TrustBadge, 
    ContactForm, 
    ProductView
)

class TagInline(admin.TabularInline):
    model = Tag
    extra = 1

@admin.register(TagType)
class TagTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'tag_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'slug')
    inlines = [TagInline]
    
    def tag_count(self, obj):
        return obj.tags.count()
    tag_count.short_description = 'Tags'

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_type', 'slug', 'product_count')
    list_filter = ('tag_type',)
    search_fields = ('name', 'slug', 'tag_type__name')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'tag_type', 'description')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

class BundleItemInline(admin.TabularInline):
    model = BundleItem
    extra = 1
    raw_id_fields = ('product',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'price', 'stock_quantity', 'views', 'created_at')
    list_filter = ('store', 'created_at')
    search_fields = ('title', 'description', 'store__name')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    readonly_fields = ('views',)
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'price', 'image', 'store', 'stock_quantity')
        }),
        ('Tags', {
            'fields': ('tags',),
        }),
        ('Analytics', {
            'fields': ('views',),
            'classes': ('collapse',),
        }),
    )

@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'available_stock', 'created_at')
    list_filter = ('store', 'created_at')
    search_fields = ('name', 'description', 'store__name')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('tags',)
    inlines = [BundleItemInline]
    
    def available_stock(self, obj):
        stock = obj.available_stock
        if stock <= 0:
            return format_html('<span style="color: red;">Out of stock</span>')
        elif stock < 5:
            return format_html('<span style="color: orange;">Low stock ({0})</span>', stock)
        else:
            return format_html('<span style="color: green;">In stock ({0})</span>', stock)
    available_stock.short_description = 'Stock'

@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'slug', 'is_published', 'updated_at')
    list_filter = ('store', 'is_published', 'updated_at')
    search_fields = ('title', 'content', 'store__name')
    prepopulated_fields = {'slug': ('title',)}
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'content', 'store', 'is_published')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',),
        }),
    )

@admin.register(TrustBadge)
class TrustBadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'badge_preview')
    list_filter = ('store',)
    search_fields = ('name', 'description', 'store__name')
    
    def badge_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" height="30" />', obj.icon.url)
        return "No image"
    badge_preview.short_description = 'Badge'

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('title', 'store', 'email_to', 'show_phone', 'show_subject', 'newsletter_integration')
    list_filter = ('store', 'show_phone', 'show_subject', 'newsletter_integration')
    search_fields = ('title', 'email_to', 'store__name')

# Register ProductView for debugging but hide from index
admin.site.register(ProductView)
admin.site.register(BundleItem)