# Generated by Django 3.0.7 on 2020-09-06 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_product_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='reserved',
            field=models.IntegerField(default=0),
        ),
    ]
