# Generated by Django 3.0.7 on 2020-08-17 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0008_preorder_expired'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='pay_pal_order',
            field=models.BooleanField(default=False),
        ),
    ]