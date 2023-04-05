from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from app.forms import CustomerRegistrationForm, CustomerProfileForm
from app.models import Product, Customer, Cart


# Create your views here.
def home(request):
    return render(request, "base/index.html", {

    })

def about(request):
    return render(request, "base/about.html", {

    })

def contact(request):
    return render(request, "base/contact.html", {

    })


class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=product[0].category).values('title')


        return render(request, 'base/category.html', locals())

class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        return render(request, 'base/product_detail.html', locals())

class CustomerRegistrationView(View):
    def get(self, request, val):
        form = CustomerRegistrationView()

        return render(request, 'base/customer_registration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratualtions!, User Register Succesfully')
        else:
            messages.warning(request, 'Invalid Input data')
        return render(request, 'base/customer_registration.html', locals())

class ProfileView(View):
    def get(self, request, val):
        form = CustomerProfileForm()
        return render(request, 'base/profile.html',locals())

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(
                user=user,
                name=name,
                locality=locality,
                city=city,
                mobile=mobile,
                state=state,
                zipcode=zipcode
            )
            reg.save()
            messages.success(request,"Congratulations! Profile saved succesfully")
        else:
            messages.warning(request,"Invalid input data")

        return render(request, 'base/profile.html', locals())


def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request, 'base/address.html', locals())

class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        return render(request, 'base/updateAddress.html', locals())
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)

        if form.is_valid():
            add = Customer.objects.get(pk = pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            # reg = Customer(
            #     user=user,
            #     name=name,
            #     locality=locality,
            #     city=city,
            #     mobile=mobile,
            #     state=state,
            #     zipcode=zipcode
            # )
            add.save()
            messages.success(request,"Congratulations! Profile saved succesfully")
        else:
            messages.warning(request,"Invalid input data")

        return redirect('address')


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('show_cart')


def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    return render(request,'base/add_to_cart.html',locals())