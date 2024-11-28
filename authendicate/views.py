from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authendicate.forms import *
from shop import views
from shop.models import *

def register(request):
    context = views.get_context_data(request.user)
    if request.user.is_authenticated:
        return redirect('home')
    context['header'] = None
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
    return redirect('login')

def login_page(request):
    context = views.get_context_data(request.user)
    if request.user.is_authenticated:
        return redirect('home')
    context['header'] = None      
    form=LoginForm()     
    if request.method=="POST":
        form=LoginForm(request.POST)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, "Login Successfully")
                return redirect('home')
    context['form'] = form
    return render(request, "authendicate/login.html", context=context)


def help_us(request):
    context = views.get_context_data(request.user)
    return render(request, "authendicate/help_us.html",context=context)


def privacy_policy(request):
    context = views.get_context_data(request.user)
    return render(request, "authendicate/privacy_policy.html",context=context)

def terms_conditions(request):
    context = views.get_context_data(request.user)
    return render(request, "authendicate/terms_conditions.html",context=context)

def user_profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = views.get_context_data(request.user)
    return render(request, "authendicate/user_profile.html",context=context)

# def update_profile(request):
#     user = request.user  # Assuming the user is authenticated
#     if request.method == 'POST':
#         user.username = request.POST.get('username', user.username)
#         user.email = request.POST.get('email', user.email)
        
#         mobile = request.POST.get('mobile', '').strip()
#         user.mobile_no = mobile if mobile else None
#         if 'profile_img' in request.FILES:
#             user.profile_img = request.FILES['profile_img']
#         user.save()
#         return redirect('user_profile')  # Redirect to the profile page

#     return render(request, 'user_profile.html', {'user': user})