# Generated by Django 3.0.7 on 2020-07-01 16:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='image_url',
        ),
    ]