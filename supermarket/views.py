from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render,get_object_or_404
from django.template.loader import get_template
from .models import Customer,Invoice
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from .forms import InvoiceForm  
from io import BytesIO
from xhtml2pdf import pisa

# from yourproject.utils import render_to_pdf


# Create your views here.
def Index(request):
    queryset = Customer.objects.filter(block_status=1).order_by('name')
    invoice = Invoice.objects.all().order_by('created_on')
    template_name = 'index.html' 
    return render(request, template_name, {'queryset':queryset,
                                            'invoice':invoice })

def CustomerDetail(request, id):
    customer = get_object_or_404(Customer, id=id)
    template_name = 'customer_details.html'
    return render(request, template_name, {'customer': customer})    

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
                subject = 'Thank you for your Order'
                message = 'we will be in touch'
                from_email = settings.EMAIL_HOST_USER
                to_list = [settings.EMAIL_HOST_USER]
                send_mail(subject,message,from_email ,to_list,fail_silently=True)
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
             'order_id': invoice.id ,
        }
        # html = template.render(context)
        pdf = render_to_pdf('invoice_pdf.html', context)
        if pdf:
            return HttpResponse(pdf, content_type='application/pdf')
        return HttpResponse("404 Not Found")    
        