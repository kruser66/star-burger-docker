# Generated by Django 3.2.15 on 2023-02-19 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0051_order_payment_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(blank=True, choices=[('cash', 'Наличные'), ('card', 'Электронно')], db_index=True, max_length=4, null=True, verbose_name='Способ оплаты'),
        ),
    ]
