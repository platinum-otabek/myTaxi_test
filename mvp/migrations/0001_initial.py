# Generated by Django 4.0.1 on 2022-01-13 16:35

import datetime
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nationality', models.CharField(default='UZ', max_length=2)),
                ('phone_number', models.CharField(default='', max_length=13)),
            ],
            options={
                'verbose_name': 'Client',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('car', models.CharField(default='malibu', max_length=63)),
                ('car_number', models.CharField(default='AA777AA', max_length=8)),
                ('phone_number', models.CharField(default='', max_length=13)),
            ],
            options={
                'verbose_name': 'Driver',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('created', 'created'), ('accepted', 'accepted'), ('finished', 'finished'), ('cancelled', 'cancelled')], default='created', max_length=10)),
                ('date', models.DateTimeField(default=datetime.datetime(2022, 1, 13, 16, 35, 12, 47735))),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.client', verbose_name='Client')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mvp.driver', verbose_name='Driver')),
            ],
        ),
    ]
