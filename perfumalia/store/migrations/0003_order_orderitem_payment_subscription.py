# Generated by Django 5.0.2 on 2024-03-18 04:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_remove_user_id_alter_user_userid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('orderStatus', models.CharField(max_length=50)),
                ('shippingDetails', models.JSONField()),
                ('orderDate', models.DateField(auto_now_add=True)),
                ('orderHistory', models.JSONField()),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.user')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('orderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('paymentID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('amount', models.FloatField()),
                ('status', models.CharField(max_length=50)),
                ('paymentDate', models.DateField()),
                ('OrderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.order')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.user')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('subscriptionID', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('subscriptionStatus', models.CharField(max_length=50)),
                ('subscriptionPlan', models.CharField(max_length=100)),
                ('nextBilling', models.DateField()),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.user')),
            ],
        ),
    ]