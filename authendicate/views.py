from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# from django.conf
from authendicate.forms import *

def register(request):

    form=RegisterForm()
    if request.method=="POST":
        form=RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful")
            return redirect('login')
        
    return render(request, "authendicate/register.html",{'form':form})

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
