# Generated by Django 3.0.7 on 2020-08-23 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0009_order_pay_pal_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_code',
            field=models.CharField(blank=True, max_length=254, null=True),
        ),
    ]