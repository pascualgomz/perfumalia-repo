from django.db import models

# Create your models here.
# Confirmar campos a borrar/modificar de order
# Confirmar tratamiento de IDs

class User(models.Model):
    userID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    cellphoneNumber = models.CharField(max_length=20)
    dateOfBirth = models.DateField()

class Order(models.Model):
    orderID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    #orderItems = models.ManyToManyField(Product, through='OrderItem')
    orderStatus = models.CharField(max_length=50)
    shippingDetails = models.JSONField()
    orderDate = models.DateField(auto_now_add=True)
    orderHistory = models.JSONField()

class OrderItem(models.Model):
    #productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)

class Payment(models.Model):
    paymentID = models.AutoField(primary_key=True)
    OrderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    status = models.CharField(max_length=50)
    paymentDate = models.DateField()

class Subscription(models.Model):
    subscriptionID = models.AutoField(primary_key=True)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    subscriptionStatus = models.CharField(max_length=50)
    subscriptionPlan = models.CharField(max_length=100)
    nextBilling = models.DateField()