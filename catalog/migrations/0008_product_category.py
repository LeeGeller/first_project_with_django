# Generated by Django 5.0.3 on 2024-04-06 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_remove_product_category_alter_product_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category_data.json',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
