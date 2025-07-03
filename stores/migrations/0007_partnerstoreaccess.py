# Generated migration for partner store access

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stores', '0006_useraddress_delete_address_order_delivery_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerStoreAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.CharField(choices=[('view', 'View Only'), ('manage', 'Full Management')], default='manage', max_length=10)),
                ('granted_at', models.DateTimeField(auto_now_add=True)),
                ('partner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stores.store')),
            ],
            options={
                'unique_together': {('partner', 'store')},
            },
        ),
    ]