from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authendicate.forms import *
from shop import views
from shop.models import *

def get_context_data(user=None):
    context = {
        'website_name' : 'indian fertilizer',
        'header' : True,
        'footer' : True,
        'cart_products' : None,
        'cart_count' : 0,
        'cart_product_ids' : set()
    }
    if user.is_authenticated:
        cart_products = Cart.objects.filter(user=user)
        context['cart_products'] = cart_products
        context['cart_product_ids'] = set(context['cart_products'].values_list('product', flat=True))
        context['cart_count'] = cart_products.count()
    return context


def register(request):
    context = views.context_data()
    form=RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect('login')
    context['form'] = form
    return render(request, "authendicate/register.html", context=context)

def logout_page(request):
    logout(request)
    messages.success(request, "Logout Successfully")
    return redirect('home')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

     if request.method=="POST":
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=name, password=pwd)
        if user is not None:
            login(request, user)
            messages.success(request, "Login Successfully")
            return redirect('home')
        else:
            messages.warning(request, "Invalid Username or Password")
            return redirect('login')
     return render(request, "shop/login.html")


def help_us(request):
    context = get_context_data(request.user)
    return render(request, "authendicate/help_us.html",context=context)


def privacy_policy(request):
    context = get_context_data(request.user)
    return render(request, "authendicate/privacy_policy.html",context=context)
