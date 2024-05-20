from django.db import models # type: ignore
from django.contrib.auth.models import User # type: ignore

class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True, blank=True)
    category_image = models.ImageField(upload_to="category/", null=True, blank=True)
    
class Item(models.Model):
    item_title = models.CharField(max_length=100, null=True, blank=True)
    item_desc = models.TextField(max_length=500, null=True, blank=True)
    item_image = models.ImageField(upload_to="item/", null=True, blank=True)
# Create your models here.


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_amount = models.IntegerField()
    image = models.ImageField(upload_to="product/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Shopping cart

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')])
    card_number = models.CharField(max_length=16, blank=True, null=True)
    expiration_date = models.CharField(max_length=5, blank=True, null=True)
    cvv = models.CharField(max_length=4, blank=True, null=True)
    total = models.CharField(max_length=16, blank=True, null=True)
    status = models.CharField(max_length=16, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)