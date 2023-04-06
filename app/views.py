import razorpay
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from app.forms import CustomerRegistrationForm, CustomerProfileForm
from app.models import Product, Customer, Cart, Payment, OrderPlaced, WishList


# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))

    return render(request, "base/index.html",locals())
@login_required
def about(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))
    return render(request, "base/about.html", locals())
@login_required
def contact(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))



    return render(request, "base/contact.html", locals())

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=product[0].category).values('title')

        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))

        return render(request, 'base/category.html', locals())
@method_decorator(login_required, name='dispatch')
class CategoryTitle(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))

        return render(request, 'base/category.html', locals())

@method_decorator(login_required, name='dispatch')
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = WishList.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))

        return render(request, 'base/product_detail.html', locals())

class CustomerRegistrationView(View):
    def get(self, request, val):
        form = CustomerRegistrationView()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))

        return render(request, 'base/customer_registration.html', locals())

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratualtions!, User Register Succesfully')
        else:
            messages.warning(request, 'Invalid Input data')
        return render(request, 'base/customer_registration.html', locals())
@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request, val):
        form = CustomerProfileForm()
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))

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
@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))

    return render(request, 'base/address.html', locals())
@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0
        wishitem = 0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))

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

@method_decorator(login_required, name='dispatch')
class checkout(View):
    def get(self, request, pk):
        totalitem = 0
        wishitem = 0

        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(WishList.objects.filter(user=request.user))

        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        razoramount = int(totalamount * 100)

        client = razorpay.Client(auth=("rzp_test_rE1xpSvaJqfMNt", "1HK3NIvUXo9bOILxaNlNEEaz"))

        data = {"amount": razoramount, "currency": "INR", "receipt": "order_rcptid_12"}
        payment_response = client.order.create(data=data)

        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user = user,
                amount=amount,
                razorpay_order_id = order_id,
                razorpay_payment_status=order_status,
            )
            payment.save()

        return render(request, 'base/checkout.html', locals())
    def post(self, request, pk):
        pass
@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect('show_cart')

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))

    return render(request,'base/add_to_cart.html',locals())

@login_required
def show_wishlist(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))

    return render(request,'base/wishlist.html',locals())


def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        product = Product.objects.filter(id=prod_id)
        amount = 0
        WishList(user=user,product=product).save()
        data = {
            'message':'Wishlist added succesfully',
        }
        return JsonResponse(data)


def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        user = request.user
        product = Product.objects.filter(id=prod_id)
        WishList(user=user,product=product).delete()
        data = {
            'message':'Wishlist removed succesfully',
        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount,
        }
        return JsonResponse(data)

@login_required
def payment_done(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(razorpay_order_id=order_id)

    payment.paid = True
    payment.razorzpy_payment_id = payment_id

    payment.save()

    cart = Cart.objects.get(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect('orders')

@login_required
def orders(request):
    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))

    order_place = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'base/orders.html', locals())

@login_required
def search(request):
    query = request.GET['search']

    totalitem = 0
    wishitem = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(WishList.objects.filter(user=request.user))

    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'base/search.html',locals())