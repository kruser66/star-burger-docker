# Generated by Django 3.2.15 on 2023-02-18 14:57

from django.db import migrations
from django.db.models import F

def fill_item_price(apps, schema_editor):
    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    items_iterator = OrderItem.objects.all().iterator()
    for item in items_iterator:
        item.price = item.product.price
        item.save()

class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_orderitem_price'),
    ]

    operations = [
        migrations.RunPython(fill_item_price)
    ]
