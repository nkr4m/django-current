from django.shortcuts import render, HttpResponse, redirect
from django.forms import inlineformset_factory
from .models import *
from django.contrib.auth.models import Group

#signup/ login imports
from .forms import OrderForm, CreateUserForm, CustomerForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import unauthenticate_user, allowed_users, admin_only

@unauthenticate_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)
            return redirect('loginPage')


    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticate_user
def loginPage(request): 
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username= username, password = password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
@admin_only
def home(request):

    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()

    context = {'orders': orders, 'customers': customers, 'total_orders' : total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', context)




@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})




@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def customers(request, pk_test):    
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count = orders.count()
    context = {'customer': customer, 'orders':orders, 'order_count':order_count}
    return render(request, 'accounts/customers.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status'), extra=5)

    customer = Customer.objects.get(id = pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form =  OrderForm(initial={'customer':customer})

    if request.method == 'POST':
        #print( 'Printing POST' request.POST)
        #formset = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect ("/")

    context = {'formset': formset}
    return render(request, "accounts/order_form.html", context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)


    form = OrderForm(instance=order)

    if request.method == 'POST':
        #print( 'Printing POST' request.POST)
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect ("/")

    context = {'form' :form}
    return render(request, "accounts/order_form.html", context)

@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect("/")

    context = {'item':order}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    delivered = orders.filter(status='delivered').count()
    pending = orders.filter(status='pending').count()
    print('Orders', orders)

    context = {'orders': orders, 'orders': orders, 'total_orders' : total_orders, 'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/user.html', context)


@login_required(login_url='loginPage')
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
    customer  = request.user.customer
    form = CustomerForm(instance= customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance= customer)
        if form.is_valid():
            form.save()

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)