from rest_framework import serializers

from applications.electronics.models import Electronic
from applications.orders.tasks import send_confirm_link
from applications.orders.models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Order
        exclude = ['confirm_code', 'order_confirm']

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.create_confirm_code()
        order.save()
        send_confirm_link.delay(order.user.email, order.confirm_code)
        return order

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        electronic = Electronic.objects.get(id=rep['electronic']).title
        rep['order_confirm'] = instance.order_confirm
        rep['electronic'] = electronic
        return rep

    def validate(self, attrs):
        electronic = attrs['electronic']
        count = attrs['count']
        if electronic.amount < count:
            raise serializers.ValidationError(f'вы не можете заказать такое количество, осталось {electronic.amount}')
        return attrs
