from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from authendicate.forms import *
from shop import views
# from django.conf import settings
# from django.core.mail import send_mail
# from .form import ForgotPasswordForm

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


# def forgot_pass(request):
#      if request.method == 'POST':
#         email = request.POST.get('email')
#         otp = request.POST.get('otp')

#         if email and not otp:
#             # Email is provided, generate and send OTP
#             form = ForgotPasswordForm(request.POST)
#             if form.is_valid():
#                 email = form.cleaned_data['email']
#                 try:
#                     user = User.objects.get(email=email)
#                     otp = random.randint(100000, 999999)
#                     request.session['otp'] = otp
#                     request.session['email'] = email

#                     # Send OTP via email
#                     send_mail(
#                         'Your OTP Code',
#                         f'Your OTP code is {otp}',
#                         settings.DEFAULT_FROM_EMAIL,
#                         [email],
#                     )
#                     messages.success(request, 'OTP has been sent to your email.')
#                 except User.DoesNotExist:
#                     messages.error(request, 'No user is associated with this email.')
#             form = ForgotPasswordForm()
        
#         elif otp:
#             # OTP is provided, verify it
#             entered_otp = request.POST.get('otp')
#             if int(entered_otp) == request.session.get('otp'):
#                 messages.success(request, 'OTP verified successfully. You can now reset your password.')
#                 return redirect('reset_password')
#             else:
#                 messages.error(request, 'Invalid OTP. Please try again.')

#         else:
#             form = ForgotPasswordForm()

#         return render(request, 'shop/products/forgot_pass.html', {'form': form, 'show_otp_field': 'otp' in request.POST})
     
# def reset_password(request):
#     if request.method == 'POST':
#         password = request.POST.get('password')
#         email = request.session.get('email')
#         if email:
#             try:
#                 user = User.objects.get(email=email)
#                 user.set_password(password)
#                 user.save()
#                 messages.success(request, 'Your password has been reset successfully.')
#                 return redirect('login')
#             except User.DoesNotExist:
#                 messages.error(request, 'Error resetting password. Please try again.')
#         else:
#             messages.error(request, 'Session expired. Please try the forgot password process again.')
#             return redirect('forgot_pass')
#     return render(request, 'shop/products/reset_password.html')sss