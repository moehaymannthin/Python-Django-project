from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=150)
    image = models.ImageField(default=None)
    price = models.IntegerField(default=None)
    qty = models.IntegerField(default=None)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, default=None)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField()

class Order(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    SUCCESS = 'success'
    CANCEL = 'cancel'
    
    ORDER_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (SUCCESS, 'Success'),
        (CANCEL, 'Cancel'),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=None)
    total_qty = models.IntegerField(default=None)
    total_price = models.IntegerField(default=None)
    name = models.CharField(max_length=30, default=None)
    phone = models.IntegerField(default=None)
    address = models.TextField(default=None)
    status = models.CharField(max_length=20,choices=ORDER_CHOICES,default='pending')
    created_at = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return str(self.id)
      

