from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from . models import *
from .forms import OrderForm
from .filters import OrderFilter
# Create your views here.

def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()

    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {'customers':customers, 'orders':orders, 'total_orders':total_orders, 'delivered':delivered, 'pending':pending}
    return render(request, 'accounts/dashboard.html',context)

def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html',{'products':products})

def customers(request,pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()

    my_filter = OrderFilter(request.GET, queryset=orders)
    orders = my_filter.qs
    context = {'customer':customer, 'orders':orders, 'orders_count':orders_count,'my_filter':my_filter}
    return render(request, 'accounts/customers.html',context)

def createOrder(request,pk):
    OrderSet = inlineformset_factory(Customer,Order, fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    #form = OrderForm(initial={'customer':customer})
    formSet = OrderSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        #print('printing post: ', request.POST)
        #form = OrderForm(request.POST)
        formSet = OrderSet(request.POST,instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('/')
    context = {'formSet':formSet}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        #print('printing post: ', request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form':form}
    return render(request, 'accounts/order_form.html', context)

def removeOrder(request,pk):
    order = Order.objects.get(id=pk)
    context = {'item':order}
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request, 'accounts/remove.html',context)