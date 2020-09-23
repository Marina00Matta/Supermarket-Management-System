from django import forms  
from .models import Invoice


class InvoiceForm(forms.ModelForm):  
    class Meta:  
        model = Invoice  
        fields = ['customer','products','shipping_address']  
        # widgets = {
        #     'customer' : forms.
        # }