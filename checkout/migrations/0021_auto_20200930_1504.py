# Generated by Django 3.0.7 on 2020-09-30 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0020_auto_20200930_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='delivery',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
