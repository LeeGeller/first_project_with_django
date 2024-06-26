# Generated by Django 5.0.3 on 2024-04-03 13:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=100, verbose_name='Название категории')),
                ('category_description', models.TextField(verbose_name='Описание категории')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100, verbose_name='Название продукта')),
                ('product_description', models.TextField(verbose_name='Описание продукта')),
                ('image_preview', models.ImageField(upload_to='catalog/', verbose_name='превью')),
                ('category_data.json', models.CharField(max_length=100, verbose_name='Категория')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена за покупку')),
                ('created_at', models.DateTimeField(verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(verbose_name='Дата последнего изменения')),
                ('connection_with_category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='catalog.category_data.json')),
            ],
            options={
                'verbose_name': 'продукт',
                'verbose_name_plural': 'продукты',
            },
        ),
    ]
