# Generated by Django 4.2.6 on 2023-11-11 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='category',
            name='keywords',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
