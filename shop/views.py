from django.shortcuts import render, redirect
from shop.models import *
from django.db.models import Avg, Count
import math
from django.contrib import messages
# from .models import productCollection
# from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
import json
# from django.conf import settings
# from django.core.mail import send_mail
# from django.contrib.auth.models import User
# import random
# from .form import ForgotPasswordForm
# from django.shortcuts import render, get_object_or_404

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

def search_view(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(name__icontains=query)
    # products = Product.objects.filter(Q(name__icontains=query) | Q(brand__icontains=query))
    products_list = list(products.values('id', 'name', 'brand'))
    return JsonResponse({'products_list': products_list})

def home(request):
    context = get_context_data(request.user)
    # Fetching trending products
    trend_produts = Product.objects.filter(is_trend=1, is_show=1)[:10].annotate(
        avg_rating = Avg('reviews__rating'),
        review_count = Count('reviews')
    )
    # Fetching most viewed products
    most_viewed_products = Product.objects.filter(is_show=1).order_by('-view_count')[:10].annotate(
        avg_rating = Avg('reviews__rating'),
        review_count = Count('reviews')
    )

    # Fetching category list
    category_list = Category.objects.all()

    context['category_list'] = category_list
    context['trend_products'] = trend_produts
    context['most_viewed_products'] = most_viewed_products
    return render(request, "shop/home.html", context=context)

def about(request):
    context = get_context_data(request.user)
    return render(request,"shop/about.html",context=context)

def add_to_cart(request, product_id=None):
    data = {}
    if request.user.is_authenticated:
        if request.method == 'POST':
            product_qty = request.POST.get('product_qty', None)
            print(request.body)
            product = Product.objects.get(id=product_id)
            if product:
                cart, created = Cart.objects.get_or_create(user=request.user, product=product)
                if cart.qty <= 9:
                    if not created:
                        cart.qty += 1
                        cart.save()

                    data['count'] = Cart.objects.filter(user=request.user).count()
                    return JsonResponse({'status' : 'success', 'message' : 'Cart added successfully.', 'data' : data}, status=200)

                return JsonResponse({'status': 'error', 'message' : 'Only 10 products added.'}, status=200)
            
            return JsonResponse({'status' : 'error', 'message' : "Product doesn't exsist."}, status=200)
        
        return JsonResponse({'status': 'error', 'message' : 'Only post method.'}, status=200)
    
    return JsonResponse({'status' : 'error', 'message' : "Please Login.", 'url' : '/login/'}, status=200)



def add_review(request, product_id=None):
    if request.user.is_authenticated:
        if product_id:
            if request.method == 'POST':
                if ProductReview.objects.filter(user=request.user, product=product_id).count() == 0:
                    feedback = request.POST.get('feedback', None)
                    rating_value = request.POST.get('ratingValue', None)
                    product = Product.objects.get(id=product_id)
                    if feedback and rating_value:
                        review, created = ProductReview.objects.get_or_create(user=request.user, product=product, review=feedback, rating=rating_value)
                        if created:
                            review.save()

            return redirect('/product_details/' + str(product_id))

        return redirect('home')

    return redirect('login')

    
def cart_page(request):
    context = get_context_data(request.user)
    if request.user.is_authenticated:
        if request.method == 'POST':
            print('delete')
        cart = Cart.objects.filter(user=request.user)
        context['cart_products'] = cart
        return render(request, "shop/cart.html", context=context)
    else:
        messages.warning(request, "Login Required")
        return redirect('login')

# # def cart_count(request):
# #     if request.user.is_authenticated:
# #         cart_count = Cart.objects.filter(user=request.user).count()
# #     else:
# #         cart_count = 0
# #     return {'cart_count': cart_count}   


def categories(request):
    context = get_context_data(request.user)
    category = Category.objects.all()
    context['category'] = category
    return render(request, "shop/categories.html",context=context)

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

def product_details(request, product_id=None):
    if product_id:
        context = get_context_data(request.user)
        product = Product.objects.get(id=product_id)
        reviews = ProductReview.objects.filter(product=product_id)
        same_products = Product.objects.filter(name__iexact=product.name)

        context['product'] = product
        context['reviews'] = reviews[:3]
        context['same_products'] = same_products
        context['has_review'] = reviews.filter(user=request.user).count() == 0 if request.user.is_authenticated else False
        try:
            context['cart_product'] = Cart.objects.get(user=request.user, product=product_id)
        except Exception:
            context['cart_product'] = None
        return render(request, "shop/product_details.html", context=context)

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



# def load_more_reviews(request):
#     product_id = request.GET.get('product_id')
#     offset = int(request.GET.get('offset', 3))
#     limit = 3  # Number of reviews to load each time

#     reviews = list(ProductReview.objects.filter(product_id=product_id)[offset:offset + limit].values())
#     return JsonResponse({'reviews': reviews})



def load_more_reviews(request):
    product_id = request.GET.get('product_id')
    offset = int(request.GET.get('offset', 3))
    limit = 3  # Number of reviews to load each time

    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    # Fetch reviews with user details, using pagination
    reviews = ProductReview.objects.filter(product=product).select_related('user')[offset:offset + limit]
    print(reviews)
    
    # Prepare the response data with specific user fields
    review_data = [
        {
            'review': review.review,
            'rating': review.rating,
            'user': {
                'username': review.user.username,
                'profile_image_url': review.user.profile_img.url  # Add more fields as needed
            }
        }
        for review in reviews
    ]

    return JsonResponse({'reviews': review_data})