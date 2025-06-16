from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HomepageBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('block_type', models.CharField(choices=[('hero_banner', 'Hero Banner'), ('product_grid', 'Product Grid'), ('featured_products', 'Featured Products'), ('testimonials', 'Testimonials'), ('text_block', 'Text Block'), ('image_gallery', 'Image Gallery'), ('newsletter_signup', 'Newsletter Signup'), ('video_embed', 'Video Embed')], max_length=50)),
                ('template_name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('description', models.TextField(blank=True)),
                ('theme_name', models.CharField(choices=[('minimal', 'Minimal'), ('dark', 'Dark'), ('warm', 'Warm')], default='minimal', max_length=50)),
                ('theme_version', models.CharField(default='v1', max_length=10)),
                ('primary_color', models.CharField(default='#3b82f6', max_length=20)),
                ('font_choice', models.CharField(choices=[('sans', 'Sans-serif'), ('serif', 'Serif'), ('mono', 'Monospace')], default='sans', max_length=20)),
                ('logo_url', models.ImageField(blank=True, null=True, upload_to='store_logos/')),
                ('custom_css', models.TextField(blank=True)),
                ('custom_js', models.TextField(blank=True)),
                ('homepage_layout', models.TextField(blank=True, default='[]')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stores', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StoreHomepageBlock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_type', models.CharField(choices=[('hero_banner', 'Hero Banner'), ('product_grid', 'Product Grid'), ('featured_products', 'Featured Products'), ('testimonials', 'Testimonials'), ('text_block', 'Text Block'), ('image_gallery', 'Image Gallery'), ('newsletter_signup', 'Newsletter Signup'), ('video_embed', 'Video Embed')], max_length=50)),
                ('order', models.PositiveIntegerField(default=0)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', models.TextField(blank=True)),
                ('configuration', models.JSONField(default=dict)),
                ('is_active', models.BooleanField(default=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='homepage_blocks', to='stores.store')),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]