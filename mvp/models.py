import datetime

import django
from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Driver(User):
    car = models.CharField(max_length=63, default='malibu')
    car_number = models.CharField(max_length=8, default='AA777AA')
    phone_number = models.CharField(max_length=13,default='')

    class Meta:
        verbose_name = 'Driver'

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'


class Client(User):
    nationality = models.CharField(max_length=2, default='UZ')
    phone_number = models.CharField(max_length=13, default='')

    class Meta:
        verbose_name = 'Client'

    def __str__(self):
        return f'{self.first_name}  {self.last_name}'


class Order(models.Model):
    STATUS = (
        ('created', 'created'),
        ('accepted', 'accepted'),
        ('finished', 'finished'),
        ('cancelled', 'cancelled'),
    )
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='Driver')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Client')
    status = models.CharField(max_length=10, default='created', choices=STATUS)
    date = models.DateTimeField(default=django.utils.timezone.now)
