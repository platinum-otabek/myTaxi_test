import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from django.test import TestCase, Client as ClientRequest


class TestDriverViews(TestCase):
    def setUp(self):
        self.client = ClientRequest()

    def test_create_driver(self):
        data = {
            'car': 'test_car',
            'car_number': '01H001AA',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        response = self.client.post('/api/v1/driver/', data=data)
        data = response.data
        assert data['first_name'] == 'test_first_name'
        assert data['last_name'] == 'test_last_name'
        assert data['username'] == 'test_username_driver'
        assert data['car'] == 'test_car'
        assert data['car_number'] == '01H001AA'
        assert data['phone_number'] == '+998977777777'

    def test_all_drivers(self):
        data = {
            'car': 'test_car',
            'car_number': '01H001AA',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        self.client.post('/api/v1/driver/', data=data)

        response = self.client.get('/api/v1/driver/')
        assert response.status_code == 200
        assert len(response.data) == 1
        data = response.data
        assert data[0]['first_name'] == 'test_first_name'
        assert data[0]['last_name'] == 'test_last_name'
        assert data[0]['username'] == 'test_username_driver'
        assert data[0]['car'] == 'test_car'
        assert data[0]['car_number'] == '01H001AA'
        assert data[0]['phone_number'] == '+998977777777'


class TestClientViews(TestCase):
    def setUp(self):
        self.client = ClientRequest()

    def test_create_client(self):
        data = {
            'nationality': 'UZ',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        response = self.client.post('/api/v1/client/', data=data)
        data = response.data
        assert data['first_name'] == 'test_first_name'
        assert data['last_name'] == 'test_last_name'
        assert data['username'] == 'test_username_driver'
        assert data['nationality'] == 'UZ'
        assert data['phone_number'] == '+998977777777'

    def test_all_clients(self):
        data = {
            'nationality': 'UZ',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        self.client.post('/api/v1/client/', data=data)

        response = self.client.get('/api/v1/client/')
        assert response.status_code == 200
        assert len(response.data) == 1
        data = response.data
        assert data[0]['first_name'] == 'test_first_name'
        assert data[0]['last_name'] == 'test_last_name'
        assert data[0]['username'] == 'test_username_driver'
        assert data[0]['nationality'] == 'UZ'
        assert data[0]['phone_number'] == '+998977777777'


class TestOrderViews(TestCase):
    def setUp(self):
        self.client = ClientRequest()

    def test_create_order(self):
        # create client
        data_client = {
            'nationality': 'UZ',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_client',
            'password': 'test'
        }
        response_client = self.client.post('/api/v1/client/', data=data_client)

        # create driver
        data_driver = {
            'car': 'test_car',
            'car_number': '01H001AA',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        response_driver = self.client.post('/api/v1/driver/', data=data_driver)
        data_order = {
            'driver': response_driver.data['id'],
            'client': response_client.data['id']
        }
        # print(f'{data_order}')
        response_order = self.client.post('/api/v1/orders/', data=data_order)
        data = response_order.data
        assert response_order.status_code == 201
        assert data['driver']['id'] == response_driver.data['id']
        assert data['client']['id'] == response_client.data['id']
        assert data['status'] == 'created'

    def test_all_clients(self):
        response_order = self.client.get('/api/v1/orders/')
        assert len(response_order.data) == 0

    def test_update_status_create(self):
        data_client = {
            'nationality': 'UZ',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_client',
            'password': 'test'
        }
        response_client = self.client.post('/api/v1/client/', data=data_client)

        # create driver
        data_driver = {
            'car': 'test_car',
            'car_number': '01H001AA',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        response_driver = self.client.post('/api/v1/driver/', data=data_driver)
        data_order = {
            'driver': response_driver.data['id'],
            'client': response_client.data['id']
        }
        # print(f'{data_order}')
        response_order = self.client.post('/api/v1/orders/', data=data_order)
        data = response_order.data
        # change status to finish and check
        update_status_finish = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                               data={'status': 'finished'},
                                               content_type='application/json'
                                               )
        assert update_status_finish.status_code == 409
        assert update_status_finish.data[
                   'msg'] == 'You can not change status from create to finish. First you can accept or cancel this order'
        # change status to cancel and check
        update_status_cancelled = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                                  data={'status': 'cancelled'},
                                                  content_type='application/json'
                                                  )

        assert update_status_cancelled.status_code == 200
        assert update_status_cancelled.data['status'] == 'cancelled'
        # change status to accept and check must be wrong
        update_status_accept = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                               data={'status': 'accepted'},
                                               content_type='application/json'
                                               )

        assert update_status_accept.status_code == 406
        assert update_status_accept.data['msg'] == 'You can not change finished or cancelled orders'

    def test_update_status_accept(self):
        data_client = {
            'nationality': 'UZ',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_client',
            'password': 'test'
        }
        response_client = self.client.post('/api/v1/client/', data=data_client)

        # create driver
        data_driver = {
            'car': 'test_car',
            'car_number': '01H001AA',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        response_driver = self.client.post('/api/v1/driver/', data=data_driver)
        data_order = {
            'driver': response_driver.data['id'],
            'client': response_client.data['id']
        }
        # print(f'{data_order}')
        response_order = self.client.post('/api/v1/orders/', data=data_order)
        data = response_order.data
        # change status from created to accepted
        update_status_accept = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                               data={'status': 'accepted'},
                                               content_type='application/json'
                                               )

        assert update_status_accept.status_code == 200

        # change status to cancel and check
        update_status_cancelled = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                                  data={'status': 'cancelled'},
                                                  content_type='application/json'
                                                  )

        assert update_status_cancelled.status_code == 409
        assert update_status_cancelled.data['msg'] == 'You can not change status from accept to cancel or create.'

        # change status to finish and check
        update_status_finish = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                               data={'status': 'finished'},
                                               content_type='application/json'
                                               )
        assert update_status_finish.status_code == 200

    def test_update_status_cancelled(self):
        data_client = {
            'nationality': 'UZ',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_client',
            'password': 'test'
        }
        response_client = self.client.post('/api/v1/client/', data=data_client)

        # create driver
        data_driver = {
            'car': 'test_car',
            'car_number': '01H001AA',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        response_driver = self.client.post('/api/v1/driver/', data=data_driver)
        data_order = {
            'driver': response_driver.data['id'],
            'client': response_client.data['id']
        }
        # print(f'{data_order}')
        response_order = self.client.post('/api/v1/orders/', data=data_order)
        data = response_order.data
        # change status to cancel and check
        update_status_cancelled = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                                  data={'status': 'cancelled'},
                                                  content_type='application/json'
                                                  )

        assert update_status_cancelled.status_code == 200
        # change status from created to accepted
        update_status_accept = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                               data={'status': 'accepted'},
                                               content_type='application/json'
                                               )
        print(update_status_accept.status_code)
        assert update_status_accept.status_code == 406
        # change status to finish and check
        update_status_finish = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                               data={'status': 'finished'},
                                               content_type='application/json'
                                               )
        assert update_status_finish.status_code == 406

    def test_update_status_finished(self):
        data_client = {
            'nationality': 'UZ',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_client',
            'password': 'test'
        }
        response_client = self.client.post('/api/v1/client/', data=data_client)

        # create driver
        data_driver = {
            'car': 'test_car',
            'car_number': '01H001AA',
            'phone_number': '+998977777777',
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'test_username_driver',
            'password': 'test'
        }
        response_driver = self.client.post('/api/v1/driver/', data=data_driver)
        data_order = {
            'driver': response_driver.data['id'],
            'client': response_client.data['id']
        }
        # print(f'{data_order}')
        response_order = self.client.post('/api/v1/orders/', data=data_order)
        data = response_order.data
        # change status from created to accepted
        self.client.put(f'/api/v1/orders/{data["id"]}/',
                        data={'status': 'accepted'},
                        content_type='application/json'
                        )
        # change status from accepted to finished
        self.client.put(f'/api/v1/orders/{data["id"]}/',
                        data={'status': 'finished'},
                        content_type='application/json'
                        )

        # change status to cancel and check
        update_status_cancelled = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                                  data={'status': 'cancelled'},
                                                  content_type='application/json'
                                                  )

        assert update_status_cancelled.status_code == 406
        # change status from created to accepted
        update_status_accept = self.client.put(f'/api/v1/orders/{data["id"]}/',
                                               data={'status': 'accepted'},
                                               content_type='application/json'
                                               )
        print(update_status_accept.status_code)
        assert update_status_accept.status_code == 406

