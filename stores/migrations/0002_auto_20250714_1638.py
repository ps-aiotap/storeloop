from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        # Add owner_username column to Store
        migrations.AddField(
            model_name='store',
            name='owner_username',
            field=models.CharField(max_length=150, default=''),
        ),
        # Remove owner foreign key if it exists
        migrations.RunSQL(
            "ALTER TABLE stores_store DROP COLUMN IF EXISTS owner_id CASCADE;",
            reverse_sql="-- No reverse"
        ),
        # Add owner_id as integer
        migrations.AddField(
            model_name='store',
            name='owner_id',
            field=models.IntegerField(default=1),
        ),
        # Update SellerProfile to be userless
        migrations.RunSQL(
            "ALTER TABLE stores_sellerprofile DROP COLUMN IF EXISTS user_id CASCADE;",
            reverse_sql="-- No reverse"
        ),
        migrations.AddField(
            model_name='sellerprofile',
            name='user_id',
            field=models.IntegerField(unique=True, default=1),
        ),
        migrations.AddField(
            model_name='sellerprofile',
            name='username',
            field=models.CharField(max_length=150, default=''),
        ),
    ]