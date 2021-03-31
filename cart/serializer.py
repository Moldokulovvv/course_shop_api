

from rest_framework import serializers

from account.models import MyUser
from cart.models import Cart
from main.models import Course
from order.models import Order


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('course', 'id' )


    def create(self, validated_data):
        request = self.context.get('request')
        customer_id = request.user.id
        # if request.user.order:
        #     print('123')
        validated_data['customer_id'] = customer_id
        b = request.data
        # print(b.get('course'))
        course = Course.objects.get(id=int(b.get('course')))

        user = MyUser.objects.get(id=request.user.id)


        if not Order.objects.filter(email=request.user.id):

            m = Order.objects.create(email=request.user, address='stop')
            m.save()
            r = Order.objects.get(email=request.user.id)
            print(type(r.id))

            validated_data['order_id'] = r.id

            cart = Cart.objects.create(**validated_data)

            return cart
        else:
            r = Order.objects.get(email=request.user.id)
            r.city += "111."
            r.save()
            print(r.id)

            cart = Cart.objects.create(order_id=r.id, **validated_data)
            return cart








