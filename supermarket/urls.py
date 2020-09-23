from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import GeneratePDF

urlpatterns = [
path('login/', auth_views.LoginView.as_view(),name='login'),
path('logout/', auth_views.LogoutView.as_view(),name='logout'),
path('', views.Index, name='home'),
path('customer/<int:id>', views.CustomerDetail, name='customer_details'),
path('invoice/<int:id>', views.InvoiceDetail, name='invoice_details'),
path('create',views.CreateInvoice, name='create'),  
# path('pdf/<int:id>',views.GeneratePDF, name='generatePDF'),
# path('customer/<int:id>/pdf/<int:id>',views.GeneratePDF.as_view()),
path('pdf/<int:id>',views.GeneratePDF.as_view()),
]
