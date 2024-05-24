# Generated by Django 5.0.3 on 2024-04-03 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_remove_product_category_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='manufactured_at',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(blank=True, default=None, max_length=100, null=True, verbose_name='Категория'),
        ),
    ]
