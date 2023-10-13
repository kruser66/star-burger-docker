from .models import Order, OrderItem
from rest_framework.serializers import ModelSerializer
from django.db import transaction


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity']


class OrderSerializer(ModelSerializer):
    products = OrderItemSerializer(many=True, allow_empty=False, write_only=True)

    def create(self, validated_data):
        order_items_data = validated_data.pop('products')
        for item in order_items_data:
            item['price'] = item['product'].price
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            order_items = [OrderItem(order=order, **item) for item in order_items_data]
            OrderItem.objects.bulk_create(order_items)

        return order

    class Meta:
        model = Order
        fields = ['id', 'products', 'firstname', 'lastname', 'address', 'phonenumber']
