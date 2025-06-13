from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_delete_seller_product_store'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveIntegerField(default=100),
        ),
        migrations.AddField(
            model_name='product',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]