# Generated by Django 3.0.7 on 2020-09-30 11:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_auto_20200930_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='weight',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(99999)]),
        ),
    ]
