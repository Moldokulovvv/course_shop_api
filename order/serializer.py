
from rest_framework import serializers

from cart.serializer import CartSerializer
from order.models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(representation)
        a = instance.cartss.all()
        print(a)
        representation['cartss'] = CartSerializer(instance.cartss.all(), many=True, context=self.context).data
        return representation
