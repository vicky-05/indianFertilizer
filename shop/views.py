from django.shortcuts import render, redirect
from shop.models import *
from django.db.models import Avg, Count, IntegerField, Value, Q
import math
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
import json
from django.db.models.functions import Cast, Coalesce

# Default context data like cart count, wedsite name, header and footer is neccessary or not and etc.
def get_context_data(user=None):
    context = {
        'website_name' : 'indian fertilizer',
        'header' : True,
        'footer' : True,
        'cart_products' : None,
        'cart_count' : 0,
        'cart_product_slugs' : set()
    }
    if user.is_authenticated:
        cart_products = Cart.objects.filter(user=user)
        context['cart_products'] = cart_products
        context['cart_product_slugs'] = set(context['cart_products'].values_list('product__slug', flat=True))
        context['cart_count'] = cart_products.count()
    return context

# Searching the Products based on it's name annd brand
def search_products(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(name__icontains=query) | Q(brand__name__icontains=query) | Q(category__name__icontains=query))
    products_list = list(products.values('slug', 'name', 'brand', 'brand__name', 'weight', 'unit_of_messure'))
    return JsonResponse({'products_list': products_list})


# Home Page
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
    
    return render(request, "shop/home.html",  context=context)

# About Page
def about(request):
    context = get_context_data(request.user)
    return render(request,"shop/about.html",context=context)



# Process of add to cart the products
def add_to_cart(request, product_slug=None):
    data = {}

    # Not login.
    if not request.user.is_authenticated:
        messages.success(request, "Please Login.")
        return JsonResponse({'messages' : 'Please login.'}, status=401)

    if request.method != 'POST':
        # Doesn't allow other methods like get, put and etc.
        return JsonResponse({'status': 'error', 'message' : 'Only post method.'}, status=200)

    if request.method == 'POST':
        product = Product.objects.get(slug=product_slug)
        
        # Product doesn't Exsist.
        if not product:
            return JsonResponse({'status' : 'error', 'message' : "Product doesn't exsist."}, status=200)

        cart, created = Cart.objects.get_or_create(user=request.user, product=product)
        if cart.qty <= 9:
            # If the product is already in cart then it will increase the qty of product
            if not created:
                cart.qty += 1
                cart.save()

            data['count'] = Cart.objects.filter(user=request.user).count()
            return JsonResponse({'status' : 'success', 'message' : 'Cart added successfully.', 'data' : data}, status=200)

        # Product quantity in cart doesn't exceed 10
        return JsonResponse({'status': 'error', 'message' : 'Quantity can not exceed 10.'}, status=200)   


# Adding reviews
def add_review(request, product_slug=None):
    if not request.user.is_authenticated:
        return redirect('login')

    if not product_slug:
        return redirect('home')

    if request.method == 'POST':
        if ProductReview.objects.filter(user=request.user, product__slug=product_slug).count() == 0:
            feedback = request.POST.get('feedback', None)
            rating_value = request.POST.get('ratingValue', 0)
            if not rating_value:
                rating_value = 0
            product = Product.objects.get(slug=product_slug)
            if feedback:
                review, created = ProductReview.objects.get_or_create(user=request.user, product=product, review=feedback, rating=rating_value)
                if created:
                    review.save()
    return redirect('/product_details/' + str(product_slug))

    

def cart_page(request):
    context = get_context_data(request.user)
    context['error_message'] = request.session.pop('error_message', None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            product_slug = request.POST.get('product_slug', None)
            print(product_slug)
            if product_slug:
                cart_product = Cart.objects.get(user=request.user, product__slug=product_slug)
                cart_product.delete()
                return redirect('cart')
        return render(request, "shop/cart.html", context=context)
    else:
        messages.warning(request, "Login Required")
        return redirect('login') 


def categories(request, category_slug=None):
    context = get_context_data(request.user)
    categories = Category.objects.filter(parent=None)
    if category_slug:
        categories = Category.objects.get(slug=category_slug)
        categories = categories.get_children()
        if not categories:
            return redirect('products', category_slug)

    context['categories'] = categories
    return render(request, "shop/categories.html",context=context)


def products(request, category_slug=None):
    context = get_context_data(request.user)
    products = Product.objects.filter(is_show=1)
    if category_slug:
        category = Category.objects.get(slug=category_slug)
        products = products.filter(category=category)
        context['category'] = category

    context['products_common_ratings'] = ProductReview.objects.order_by('rating').values_list('rating', flat=True).distinct()
    context['categories'] = Category.objects.all()
    context['brands'] = Brand.objects.all()
    return render(request, 'shop/products.html', context=context)


def product_details(request, product_slug=None):
    if product_slug:
        context = get_context_data(request.user)
        product = Product.objects.get(slug=product_slug)
        
        # FFor Incresing View Count
        session_key = f'/product_details/{product_slug}'

        if not request.session.get(session_key):
            # Increment the view count if the product hasn't been viewed
            product.view_count += 1
            product.save()

            # Mark the product as viewed in the session
            request.session[session_key] = True

        reviews = ProductReview.objects.filter(product__slug=product_slug)
        different_weight_products = Product.objects.filter(name__iexact=product.name)
        similar_products = Product.objects.filter(is_show=1).filter(Q(name__icontains=product.name) | Q(category__name__icontains=product.category.name) | Q(brand__name__icontains=product.brand.name))

        context['product'] = product
        context['reviews'] = reviews[:3]
        context['similar_products'] = similar_products.annotate(
            avg_rating = Avg('reviews__rating'),
            review_count = Count('reviews')
        )[:10]
        context['different_weight_products'] = different_weight_products.values('slug', 'weight', 'unit_of_messure')
        context['has_review'] = reviews.filter(user=request.user).count() == 0 if request.user.is_authenticated else False
        try:
            context['cart_product'] = Cart.objects.get(user=request.user, product__slug=product_slug)
        except Exception:
            context['cart_product'] = None
        return render(request, "shop/product_details.html", context=context)


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


def get_products(request):
    context = get_context_data(request.user)
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        brand_ids = request.GET.getlist('brands[]', None)
        rating = request.GET.get('rating', None)
        category = request.GET.get('category', None)
        price_range = request.GET.get('price_range', None)
        offset = int(request.GET.get('offset', 0))   # Number of offset like page no
        limit = int(request.GET.get('limit', 9))  # Number of products to load each time

        products = Product.objects.order_by('name').filter(is_show=1).annotate(
            avg_rating = Coalesce(Cast(Avg('reviews__rating'), IntegerField()), Value(0)),
            review_count = Count('reviews')
        )

        # Filtering Conditions
        # Brand Filtering
        if brand_ids:
            products = products.filter(brand__id__in=brand_ids)

        # Rating Filtering
        if rating == '1':
            products = products.filter(avg_rating__gte=1)
            print(products)
        elif rating == '2':
            products = products.filter(avg_rating__gte=2)
        elif rating == '3':
            products = products.filter(avg_rating__gte=3)
        elif rating == '4':
            products = products.filter(avg_rating__gte=4)
        elif rating == '5':
            products = products.filter(avg_rating=5)

        # Category Filtering
        if category:
            products = products.filter(category__slug=category)
        
        # Price Range Filtering
        if price_range == 'low':
            products = products.filter(selling_price__lt=50)
        elif price_range == 'medium':
            products = products.filter(selling_price__range=(50, 100))
        elif price_range == 'high':
            products = products.filter(selling_price__gt=100)

        # Apply pagination by slicing the queryset
        products = products[offset:offset + limit]    

        products_data = list(products.values('slug', 'name', 'category__name', 'brand__name', 'image', 'unit_of_messure', 'weight', 'discount_price', 'discount_percentage', 'mrp_price', 'selling_price', 'avg_rating', 'review_count'))

        return JsonResponse({'products': products_data, 'cart_product_slugs': list(context['cart_product_slugs'])})

def update_product_qty(request, product_slug=None, action=None):
    try:
        product = Product.objects.get(slug=product_slug)
        cart = Cart.objects.get(user=request.user, product=product)

        if action == 'increase':
            if cart.qty <= 9:
                cart.qty += 1
            else:
                print('hii')
                request.session['error_message'] = "Quantity can not exceed 10."
        elif action == 'decrease' and cart.qty > 1:
            cart.qty -= 1
        cart.save()
    except Exception as e:
        pass

    return redirect('cart')