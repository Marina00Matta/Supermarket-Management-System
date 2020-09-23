from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Customer,Product,Invoice
# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Invoice) 
admin.site.unregister(Group) 

admin.site.site_header = "Super Market Management System"

