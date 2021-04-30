from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem, Order
from django.contrib.auth.models import Group, User
from .forms import SignUpForm, OrderForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout

# Create your views here.
def home(request, category_slug=None):
    category_page = None
    products = None

    if category_slug != None:
        category_page = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category_page, available=True)
    else:
        products = Product.objects.all().filter(available=True)

    return render(request, 'shop/home.html', {'category': category_page, 'products': products})


def product(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
    except Exception as e:
        raise e
    return render(request, 'shop/product.html', {'product': product})


def _cart_id(request):  # за допомогою framework session ми можемо зберігати наш кошик
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart  # повертає cart (кошик) сесію


def add_cart(request, product_id):  # добавляє продукт
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # получает обьект из текущей сесии, если он существует
    except Cart.DoesNotExist:  # якщо корзина не ісує, то її створять
        cart = Cart.objects.create(cart_id=_cart_id(request))  # створює об'єк, якщо його немає
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) # якщо об'єкт вже є в корзині,
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1  # то просто добавиться +1 до кількості
        cart_item.save()
    except CartItem.DoesNotExist: # якщо не існує, то створиться в корзині новий продукт
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect('cart_detail')


def cart_detail(request, total=0, counter=0, cart_items=None): #  витягує всі продукти, і калькулює всю суму за товар
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # ми пробуємо получити об'єкт cart
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter += cart_item.quantity
    except ObjectDoesNotExist:
        pass

    return render(request, 'shop/cart.html', dict(cart_items=cart_items, total=total, counter=counter))


def cart_remove(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id) # знаходимо продукт, кількість якого ми хочемо обновити
    cart_item = CartItem.objects.get(product=product, cart=cart)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')


def cart_remove_product(request, product_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id) # знаходимо продукт, кількість якого ми хочемо обновити
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart_detail')


def add_product(request, product_id):  # добавляє продукт
    product = Product.objects.get(id=product_id)
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))  # получает обьект из текущей сесии, если он существует
    except Cart.DoesNotExist:  # якщо корзина не ісує, то її створять
        cart = Cart.objects.create(cart_id=_cart_id(request))  # створює об'єк, якщо його немає
        cart.save()
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart) # якщо об'єкт вже є в корзині,
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity += 1  # то просто добавиться +1 до кількості
        cart_item.save()
    except CartItem.DoesNotExist: # якщо не існує, то створиться в корзині новий продукт
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()
    return redirect('home')


def signUpView(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            user_group = Group.objects.get(name='User')
            user_group.user_set.add(signup_user)
    else:
        form = SignUpForm()
    return render(request, 'shop/signup.html', {'form': form})


def loginView(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None: # якщо такий юзер інсує, то ми логінимо
                login(request, user)
                return redirect('home')
            else:
                return redirect('signup')
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})


def logoutView(request):
    logout(request)
    return redirect('login')


def order(request):
    category = Category.objects.all()
    curent_user = request.user
    orders = CartItem.objects.filter(cart_id=curent_user.id)
    context = {'category': category,
               'orders': orders,
               }
    return render(request, 'shop/orders.html', context)


def createOrder(request):
    form = OrderForm()

    error = ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order')
        else:
            error = 'Форма не вірна'

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'shop/cart.html', data)