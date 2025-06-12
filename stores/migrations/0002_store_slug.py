from django.db import migrations, models
import django.utils.text

def generate_slugs(apps, schema_editor):
    Store = apps.get_model('stores', 'Store')
    for store in Store.objects.all():
        store.slug = django.utils.text.slugify(store.name)
        store.save()

class Migration(migrations.Migration):

    dependencies = [
        ('stores', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='slug',
            field=models.SlugField(max_length=100, null=True),
        ),
        migrations.RunPython(generate_slugs),
        migrations.AlterField(
            model_name='store',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]