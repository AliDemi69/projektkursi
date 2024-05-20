from django.http import JsonResponse
from django.shortcuts import  render, redirect
from .models import *
from .forms import CheckoutForm, RegistrationForm, LoginForm, SearchForm
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


def home(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    items = Item.objects.all()
    cart_items = CartItem.objects.all()
    all_products = Product.objects.all()
    categories = Category.objects.all()
    paginator = Paginator(all_products, 8)

    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:

        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    context = {"items":items, 'products': products, 'user': user , 'cart_items' : cart_items , 'categories' : categories}
    return render(request, 'home.html', context)

def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {"categories" : categories})

def terms(request):
    categories = Category.objects.all()
    return render(request, 'terms.html', {"categories" : categories})

def privacy(request):
    categories = Category.objects.all()
    return render(request, 'privacy.html', {"categories" : categories})

# signup page
def user_register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.create()
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

# logout page
def user_logout(request):
    logout(request)
    return redirect('login')

# Search

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = request.GET['query']
            results = Product.objects.filter(name__icontains=query)
            return render(request, 'search_results.html', {'results': results, 'query': query})
    return render(request, 'search_results.html')

# Shopping Cart

def add_to_cart(request, product_id):
    product = Product.objects.get(pk=product_id)
    user_id=request.user.id
    cart_item, created = CartItem.objects.get_or_create(product=product,user_id=user_id)
    cart_item.quantity += 1
    cart_item.save()
    return JsonResponse({'message': "Item added to cart"})

def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(pk=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')

def view_cart(request):
    cart_items = CartItem.objects.select_related('product').all()
    categories = Category.objects.all()
    

    total_price = 0
    for cart_item in cart_items:
        # Calculate total price
        total_price += cart_item.product.price * cart_item.quantity

    context = {'cart_items': cart_items, 'total_price': total_price, "categories": categories}
    return render(request, 'view_cart.html', context)

def update_cart_item(request, cart_item_id):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(pk=cart_item_id)
        new_quantity = int(request.POST.get('quantity', 0))

        # Check if action is decrement
        if request.POST.get('action') == 'decrement':
            if new_quantity > 1:
                cart_item.quantity = new_quantity - 1
                cart_item.save()
        else:
            cart_item.quantity = new_quantity + 1
            cart_item.save()

    return redirect('view_cart')
    

def checkout(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            user_id = request.user.id
            order = Order.objects.create(
                user_id=user_id,
                full_name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                country=form.cleaned_data['country'],
                payment_method=form.cleaned_data['payment_method'],
                card_number=form.cleaned_data.get('card_number', None),
                expiration_date=form.cleaned_data.get('expiration_date', None),
                cvv=form.cleaned_data.get('cvv', None),
            )
            cart_items = CartItem.objects.filter(user_id=user_id)
            for item in cart_items:
                OrderProducts.objects.create(order=order, product=item.product)
            
            cart_items.delete()

            if cart_items.exists():
                return redirect('view_cart')
            else:
                return render(request, 'empty_cart_view.html')
        
    else:
        form = CheckoutForm()

    return render(request, 'view_cart.html', {'form': form, "categories": categories})


def order_history(request):
    orders = Order.objects.filter(user=request.user)
    categories = Category.objects.all()
    cart_items = CartItem.objects.all()

    products_by_order = {}
    for order in orders:
        order_products = OrderProducts.objects.filter(order=order)
        products_by_order[order.id] = [order_product.product for order_product in order_products]
        
    return render(request, 'order_history.html', {'orders': orders, 'order_products': products_by_order , "categories" : categories, "cart_items": cart_items})



def filter_products_by_category(request, category_id):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
        categories = Category.objects.all()
        cart_items = CartItem.objects.all()
        return render(request, 'product_list.html', {'products': products, "categories" : categories, "cart_items": cart_items})
    else:
        return JsonResponse({'error': 'Category ID not provided'})

def get_all_products(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    items = Item.objects.all()
    cart_items = CartItem.objects.all()
    all_products = Product.objects.all()
    categories = Category.objects.all()

    context = {"items":items, 'products': all_products, 'user': user , 'cart_items' : cart_items , 'categories' : categories}
    return render(request, 'best_deals.html', context)