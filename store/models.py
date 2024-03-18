from django.db import models

class User(models.Model):
    userID = models.CharField(primary_key = True, max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    cellphoneNumber = models.CharField(max_length=100)
    dateOfBirth = models.DateField()


class Perfume(models.Model):
    productID = models.CharField(primary_key = True, max_length=100)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.IntegerField()
    inventoryQuantity = models.IntegerField()
    details = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class ShoppingCart(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    items = models.JSONField(blank=True, default=list)
    quantity = models.IntegerField()
    subtotal = models.CharField(max_length=100)
    savedForLater = models.JSONField(blank=True, default=list)

    def __str__(self):
        return str(self.userID)
    
class Recommendations(models.Model):
    userID = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    purchaseHistory = models.JSONField(blank=True, default=list)
    browsingHistory = models.JSONField(blank=True, default=list)
    recommendationList = models.JSONField(blank=True, default=list)

    def __str__(self):
        return str(self.userID)