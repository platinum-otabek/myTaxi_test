from rest_framework import serializers

from mvp.models import Driver, Client, Order


class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ('id', 'last_name', 'first_name', 'car', 'car_number', 'phone_number', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        driver = Driver.objects.create(**validated_data)
        driver.set_password(validated_data['password'])
        driver.save()
        return driver


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'last_name', 'first_name', 'nationality', 'phone_number', 'username', 'password',)
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        client = Client.objects.create(**validated_data)
        client.set_password(validated_data['password'])
        client.save()
        return client


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'driver', 'client', 'status', 'date')

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['driver'] = DriverSerializer(instance.driver).data
        response['client'] = ClientSerializer(instance.client).data
        return response

    def create(self, validated_data):
        order = Order.objects.create(**validated_data)
        order.save()
        return order
