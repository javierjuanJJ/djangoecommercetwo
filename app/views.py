from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from app.forms import CustomerRegistrationForm
from app.models import Product


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
        return render(request, 'base/profile.html',locals())

    def post(self, request):
        return render(request, 'base/profile.html', locals())