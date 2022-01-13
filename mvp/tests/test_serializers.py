import os
from collections import OrderedDict

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.test import TestCase

from mvp.models import Driver, Client, Order
from mvp.serializers import DriverSerializer, ClientSerializer, OrderSerializer


class TestDriverSerializer(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create(car='test_car',
                                            car_number='01H001AA',
                                            phone_number='+998977777777',
                                            first_name='test_first_name',
                                            last_name='test_last_name',
                                            username='test_username_driver'
                                            )

    def test_data(self):
        data = DriverSerializer(self.driver).data
        assert data['first_name'] == 'test_first_name'
        assert data['last_name'] == 'test_last_name'
        assert data['username'] == 'test_username_driver'
        assert data['car'] == 'test_car'
        assert data['car_number'] == '01H001AA'
        assert data['phone_number'] == '+998977777777'


class TestClientSerializer(TestCase):
    def setUp(self) -> None:
        self.client = Client.objects.create(nationality='UZ',
                                            phone_number='+998977777777',
                                            first_name='test_first_name',
                                            last_name='test_last_name',
                                            username='test_username_client'
                                            )

    def test_data(self):
        data = ClientSerializer(self.client).data
        assert data['first_name'] == 'test_first_name'
        assert data['last_name'] == 'test_last_name'
        assert data['username'] == 'test_username_client'
        assert data['nationality'] == 'UZ'
        assert data['phone_number'] == '+998977777777'


class TestOrderSerializer(TestCase):
    def setUp(self) -> None:
        self.driver = Driver.objects.create(car='test_car',
                                            car_number='01H001AA',
                                            phone_number='+998977777777',
                                            first_name='test_first_name',
                                            last_name='test_last_name',
                                            username='test_username_driver'
                                            )
        self.client = Client.objects.create(nationality='UZ',
                                            phone_number='+998977777777',
                                            first_name='test_first_name',
                                            last_name='test_last_name',
                                            username='test_username_client'
                                            )
        self.order = Order.objects.create(driver=self.driver,
                                          client=self.client)

    def test_data(self):
        data = OrderedDict(OrderSerializer(self.order).data)
        assert data['driver']['first_name'] == self.driver.first_name
        assert data['client']['first_name'] == self.client.first_name
        assert data['status'] == 'created'
