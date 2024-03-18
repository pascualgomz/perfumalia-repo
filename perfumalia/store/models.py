from django.db import models

# Create your models here.

class User(models.Model):
    userID = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    cellphoneNumber = models.CharField(max_length=20)
    dateOfBirth = models.DateField()