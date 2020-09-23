from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from .models import Customer,Invoice
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from .forms import InvoiceForm  
from io import BytesIO
from xhtml2pdf import pisa



# Create your views here.


# {% if user.is.authenticated %}

def Index(request):
    queryset = Customer.objects.filter(block_status=1).order_by('name')
    invoice = Invoice.objects.all().order_by('created_on')
    template_name = 'index.html' 
    return render(request, template_name, {'queryset':queryset,
                                            'invoice':invoice })
def CustomerDetail(request, id):
    customer = get_object_or_404(Customer, id=id)
    invoice = Invoice.objects.all().filter(customer_id = id)
    template_name = 'customer_details.html'
    return render(request, template_name, {'customer': customer,
                                            'invoice': invoice
                                                                })    


def InvoiceDetail(request, id):
    invoice = get_object_or_404(Invoice, id=id)
    template_name = 'invoice_details.html'
    return render(request, template_name,{'invoice': invoice})


def CreateInvoice(request):  
    if request.method == "POST":  
        form = InvoiceForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                reciept = EmailInvoiceContent()
                subject = 'My Supermarket - Thank you for your Order'
                html_message = 'Hey, this is your reciept for your order'+reciept
                plain_message = strip_tags(html_message)
                from_email = settings.EMAIL_HOST_USER
                to_email  = 'marinamedhat_19@hotmail.com'
                mail.send_mail(subject,plain_message,from_email ,to_email,html_message=html_message,fail_silently=False)
                return redirect('/')  
            except:  
                pass  
    else:  
        form = InvoiceForm()  
    template_name = 'create.html'
    return render(request,template_name,{'form':form})  

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class GeneratePDF(View):
    def get(self, request, id, *args, **kwargs):
        invoice = Invoice.objects.get(id=id)
        total_price = 0
        for product in invoice.products.all():
            total_price += product.price
           
        context = { 
             'amount': total_price,
             'customer_name': invoice.customer.name,
             'products': invoice.products.all,
             'address' : invoice.shipping_address,
             'created_on' : invoice.created_on,
        }
        # html = template.render(context)
        pdf = render_to_pdf('invoice_pdf.html', context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("404 Not Found")    


def EmailInvoiceContent():
    invoice = Invoice.objects.latest()
    context = { 
             'customer_name': invoice.customer.name,
             'products': invoice.products.all,
             'address' : invoice.shipping_address,
             'created_on' : invoice.created_on,
        }   
    pdf = render_to_string('invoice_pdf.html', context)
    if pdf:
        return HttpResponse(pdf, content_type='application/pdf')
    return HttpResponse("404 Not Found")  
    
