from . import views
from django.urls import path
# from .views import GeneratePDF

urlpatterns = [
path('', views.Index, name='home'),
path('customer/<int:id>', views.CustomerDetail, name='customer_details'),
path('invoice/<int:id>', views.InvoiceDetail, name='invoice_details'),
path('create',views.CreateInvoice, name='create'),  
path('pdf/<int:id>',views.GeneratePDF.as_view())

]
