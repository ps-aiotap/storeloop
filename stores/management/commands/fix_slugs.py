from django.core.management.base import BaseCommand
from django.utils.text import slugify
from stores.models import Store

class Command(BaseCommand):
    help = 'Fix duplicate store slugs'

    def handle(self, *args, **options):
        stores = Store.objects.all()
        fixed_count = 0
        
        for store in stores:
            if not store.slug or store.slug == 'default-store':
                base_slug = slugify(store.name) or f'store-{store.id}'
                slug = base_slug
                counter = 1
                
                # Ensure unique slug
                while Store.objects.filter(slug=slug).exclude(pk=store.pk).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                old_slug = store.slug
                store.slug = slug
                store.save()
                fixed_count += 1
                self.stdout.write(f"Updated store '{store.name}': '{old_slug}' -> '{slug}'")
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully fixed {fixed_count} store slugs')
        )