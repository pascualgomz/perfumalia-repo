# Generated by Django 5.0.2 on 2024-03-18 04:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_order_orderitem_payment_subscription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='orderID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='payment',
            name='paymentID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='subscriptionID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='userID',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
