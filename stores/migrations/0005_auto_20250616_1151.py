from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        (
            "stores",
            "0004_alter_store_custom_css_alter_store_custom_js_and_more",
        ),  # Make sure this matches your last migration
    ]

    operations = [
        migrations.CreateModel(
            name="HomepageBlock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "block_type",
                    models.CharField(
                        choices=[
                            ("hero_banner", "Hero Banner"),
                            ("product_grid", "Product Grid"),
                            ("featured_products", "Featured Products"),
                            ("testimonials", "Testimonials"),
                            ("text_block", "Text Block"),
                            ("image_gallery", "Image Gallery"),
                            ("newsletter_signup", "Newsletter Signup"),
                            ("video_embed", "Video Embed"),
                        ],
                        max_length=50,
                    ),
                ),
                ("template_name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="StoreHomepageBlock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "block_type",
                    models.CharField(
                        choices=[
                            ("hero_banner", "Hero Banner"),
                            ("product_grid", "Product Grid"),
                            ("featured_products", "Featured Products"),
                            ("testimonials", "Testimonials"),
                            ("text_block", "Text Block"),
                            ("image_gallery", "Image Gallery"),
                            ("newsletter_signup", "Newsletter Signup"),
                            ("video_embed", "Video Embed"),
                        ],
                        max_length=50,
                    ),
                ),
                ("order", models.PositiveIntegerField(default=0)),
                ("title", models.CharField(blank=True, max_length=200)),
                ("content", models.TextField(blank=True)),
                ("configuration", models.JSONField(default=dict)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "store",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="homepage_blocks",
                        to="stores.store",
                    ),
                ),
            ],
            options={
                "ordering": ["order"],
            },
        ),
    ]
