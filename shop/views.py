from django.shortcuts import render
# from .models import *
# from django.contrib import messages
# from django.shortcuts import redirect
# from .models import productCollection
# from django.contrib.auth import authenticate, login, logout
# from django.http import JsonResponse
# import json
# from django.conf import settings
# from django.core.mail import send_mail
# from django.contrib.auth.models import User
# import random
# from .form import ForgotPasswordForm
# from django.shortcuts import render, get_object_or_404
# # Create your views here.

# def home(request):
#     trend = trend_products.objects.filter(status=0)
#     return render(request, "shop/index.html",{'trend':trend})

# def add_cart(request):
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         if request.user.is_authenticated:
#             data = json.loads(request.body)
#             product_qty = data['product_qty']
#             product_id = data['pid']
#             product_status = productCollection.objects.get(id=product_id)
#             if product_status:
#                 if Cart.objects.filter(user=request.user.id, product_id=product_id).exists():
#                     return JsonResponse({'status': 'Product already in cart'}, status=200)
                    
#                 else:
#                     if product_status.quantity >= product_qty:
#                         Cart.objects.create(user=request.user, product_id=product_id, product_qty=product_qty)
#                         return JsonResponse({'status': 'Product added to cart successfully'}, status=200)
                        
#                     else:
#                         return JsonResponse({'status': 'Product out of stock'}, status=200)
#             else:
#                 return JsonResponse({'status': 'Product not found'}, status=200)
#         else:
#             return JsonResponse({'status': 'Login Required'}, status=200)
            
#     else:
#         return JsonResponse({'status': 'error'}, status=200)
    
# def cart_page(request):
#     if request.user.is_authenticated:
#         cart = Cart.objects.filter(user=request.user)
#         cart_count = cart.count()
#         return render(request, "shop/products/add_to_cart.html",{'cart':cart})
#     else:
#         messages.warning(request, "Login Required")
#         return redirect('login')

# # def cart_count(request):
# #     if request.user.is_authenticated:
# #         cart_count = Cart.objects.filter(user=request.user).count()
# #     else:
# #         cart_count = 0
# #     return {'cart_count': cart_count}   


# def categories(request):
#     category = Category.objects.filter(status=0)
#     return render(request, "shop/categories.html",{'category':category})

# # def home(request):
# #     topBrands = TopBrands.objects.filter(status=0)
# #     return render(request, "shop/index.html",{'topBrands':topBrands})

# def collections(request):
#     return render(request, "shop/products/index.html")

# def collectionsview(request,group_name):
#     if(Category.objects.filter(product_title=group_name,status=0)):
#         productcollection = productCollection.objects.filter(group_name=group_name)
#         return render(request, "shop/products/index.html",{'productcollection':productcollection,'group_names':group_name})
#     else:
#         return redirect('collections')

# def product_details(request, cname, pname):
#     if Category.objects.filter(product_title=cname, status=0):
#         if productCollection.objects.filter(name_product=pname, status=0):
#             products = productCollection.objects.filter(name_product=pname, status=0).first()
#             return render(request, "shop/products/products_details.html", {'products': products})
#         else:
#             return redirect('collections')

# def collections(request):
#     # Retrieve distinct brand names
#     distinct_brand_names = productCollection.objects.values('brand_name').distinct()

#     # Pass the brand names to the template
#     return render(request, 'collections.html', {'distinct_brand_names': distinct_brand_names})

# def product_detail(request, product_id):
#     product = productCollection.objects.get(id=product_id)
#     return render(request, 'product_detail.html', {'product': product})

# def product_detailss(request, pnme):
#     if productCollection.objects.filter(name_product=pnme, status=0):
#             products = productCollection.objects.filter(name_product=pnme, status=0).first()
#             return render(request, "shop/products/products_details.html", {'products': products})
#     else:
#             return redirect('collections')




# def user_profile(request):
#     return render(request, 'shop/user_profile.html')

# def remove_cart(request,cid):
#     cartitem = Cart.objects.get(id=cid)
#     cartitem.delete()
#     return redirect('/cart')


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
#     return render(request, 'shop/products/reset_password.html')