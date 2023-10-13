# Generated by Django 3.2.15 on 2023-02-18 14:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0042_alter_order_lastname'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=8, validators=[django.core.validators.MinValueValidator(0)], verbose_name='цена'),
            preserve_default=False,
        ),
    ]
