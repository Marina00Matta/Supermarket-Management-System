from django.db import models
# from django.urls import reverse
# from phone_field import PhoneField


# Create your models here.
STATUS = (
    (0,"Blocked"),
    (1,"Active")
)

class Customer(models.Model):
    name = models.CharField(max_length=30,blank = False, null = False)
    phone = models.CharField(max_length=30,blank=True)
    email = models.EmailField(max_length=100)
    address = models.TextField(blank = True)
    block_status = models.IntegerField(choices=STATUS, default=1) 
    
    def __str__(self):
        return self.name 

class Product(models.Model):
    name = models.CharField(max_length=30,blank = False, null = False)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.DO_NOTHING)   
    products = models.ManyToManyField(Product)
    # shipping_address = models.ForeignKey(Customer,on_delete=models.CASCADE)
    shipping_address = models.TextField(blank= False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_on)