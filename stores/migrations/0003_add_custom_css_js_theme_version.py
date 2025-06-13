from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0002_store_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='custom_css',
            field=models.TextField(blank=True, help_text='Custom CSS to be injected into store pages', null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='custom_js',
            field=models.TextField(blank=True, help_text='Custom JavaScript to be injected into store pages', null=True),
        ),
        migrations.AddField(
            model_name='store',
            name='theme_version',
            field=models.CharField(default='v1', help_text='Theme version to use for this store', max_length=10),
        ),
    ]