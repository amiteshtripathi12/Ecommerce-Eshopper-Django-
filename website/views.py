from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
import json
from django.utils.decorators import method_decorator
from django.db.models import Max, Min, Count, Avg
from django.db.models.functions import ExtractMonth
from django.views import View
from .models import Slider, Product, Theme, Cart, Sideofferbar, ReviewRating, Customer, Wishlist, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
import re
from .forms import CustomerRegistrationForm, ReviewForm, CustomerProfileForm
from django.contrib.auth import authenticate, login
from .utils import cookieCart, cartData, guestOrder
from datetime import datetime


# from django.contrib.auth import authenticate, login

class ProductView(View):
    @staticmethod
    def get(request):
        # totalitem = 0
        sideofferbar = Sideofferbar.objects.all()
        feature_item = Product.objects.filter(category='WOMENS')
        sunglasses = Product.objects.filter(category="SUNGLASSES")
        tshirt = Product.objects.filter(category="MENS").filter(subcategory='T-Shirt')
        blazer = Product.objects.filter(category="MENS").filter(subcategory='Blazer')
        kids = Product.objects.filter(category="KIDS")
        recommended = Product.objects.filter(Brand='FENDI')
        fendi = Product.objects.filter(Brand='FENDI').count()
        albiro = Product.objects.filter(Brand='ALBIRO').count()
        acne = Product.objects.filter(Brand='ACNE').count()
        underarmour = Product.objects.filter(Brand='UNDERARMOUR').count()
        prada = Product.objects.filter(Brand='PRADA').count()
        chanel = Product.objects.filter(Brand='CHANEL').count()
        gucci = Product.objects.filter(Brand='GUCCI').count()
        recommended1 = Product.objects.filter(Brand='ACNE')
        slideimage = Slider.objects.all()
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(user=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            cookieData = cookieCart(request)
            cartItems = cookieData['cartItems']
            order = cookieData['order']
            items = cookieData['items']
        return render(request, 'index.html', {'slideimage': slideimage, 'feature_item': feature_item,
                                              'sunglasses': sunglasses, 'tshirt': tshirt, 'blazer': blazer,
                                              'kids': kids, 'recommended': recommended, 'recommended1': recommended1,
                                              'sideofferbar': sideofferbar, 'fendi': fendi, 'albiro': albiro,
                                              'gucci': gucci,
                                              'chanel': chanel, 'prada': prada, 'underarmour': underarmour,
                                              'acne': acne, 'cartItems': cartItems, 'items': items})


def theme(request):
    pass


'''def index(request):
    slideimage = Slider.objects.all()
    return render(request, 'index.html', {'slideimage': slideimage})
'''


def about(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return render(request, 'about.html', {'cartItems': cartItems, 'items': items})


def shop(request):
    # sideofferbar = Sideofferbar.objects.all()
    global items
    allproducts = Product.objects.all()
    fendi = Product.objects.filter(Brand='FENDI').count()
    albiro = Product.objects.filter(Brand='ALBIRO').count()
    acne = Product.objects.filter(Brand='ACNE').count()
    underarmour = Product.objects.filter(Brand='UNDERARMOUR').count()
    prada = Product.objects.filter(Brand='PRADA').count()
    chanel = Product.objects.filter(Brand='CHANEL').count()
    gucci = Product.objects.filter(Brand='GUCCI').count()
    sideofferbar = Sideofferbar.objects.all()

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
    return render(request, 'shop.html', {'allproducts': allproducts, 'fendi': fendi, 'albiro': albiro,
                                         'gucci': gucci, 'sideofferbar': sideofferbar,
                                         'chanel': chanel, 'prada': prada, 'underarmour': underarmour,
                                         'acne': acne, 'items': items, 'cartItems': cartItems})


def blog(request):
    return render(request, 'blog.html', {})


def blog_single(request):
    return render(request, 'blog-single.html', {})


def cart(request):
    return render(request, 'cart.html', {})


@login_required()
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    # product_id = request.GET.get('prod_id')
    # product = Product.objects.get(id=product_id)
    amount = 0.0
    shipping_amount = 2.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user ==
                    request.user]
    if cart_product:
        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount
    return render(request, 'checkout.html', {'add': add,
                                             'totalamount': totalamount, 'cart_items': cart_items})


@method_decorator(login_required, name='dispatch')
class CheckoutView(View):
    def get(self, request):
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        user = request.user
        add = Customer.objects.filter(user=user)
        # Cart(product=product).save()
        # global totalitem
        # product = Product.objects.filter(user=request.user)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            # item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
        return render(request, 'checkout1.html',
                      {'product': product, 'add': add})


def contact_us(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']

        return render(request, 'contact-us.html', {'name': name})
    else:
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(user=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            cookieData = cookieCart(request)
            cartItems = cookieData['cartItems']
            order = cookieData['order']
            items = cookieData['items']
        return render(request, 'contact-us.html', {'cartItems': cartItems, 'items': items})


'''
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['first_name']
        lastname = request.POST['last_name']
        email = request.POST.get('email_id')
        password = request.POST['password']
        x = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=email,
                                     password=password)
        x.save()
        messages.success(request, " Your id has been successfully created")
        return render(request, 'customerregistration.html')

    else:
        messages.error(request, "Not a valid password!")
        return render(request, 'blog.html')

'''


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm
        return render(request, 'customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            messages.success(request, 'User Registered Successfully')
            form.save()
        return render(request, 'customerregistration.html', {'form': form})


class ProductDetailView(View):
    def get(self, request, prod_id):
        global item_already_in_cart, product
        details = Product.objects.filter(Brand='ACNE')
        kids = Product.objects.filter(category="KIDS")
        recommended = Product.objects.filter(Brand='FENDI')
        fendi = Product.objects.filter(Brand='FENDI').count()
        albiro = Product.objects.filter(Brand='ALBIRO').count()
        acne = Product.objects.filter(Brand='ACNE').count()
        underarmour = Product.objects.filter(Brand='UNDERARMOUR').count()
        prada = Product.objects.filter(Brand='PRADA').count()
        chanel = Product.objects.filter(Brand='CHANEL').count()
        gucci = Product.objects.filter(Brand='GUCCI').count()
        recommended1 = Product.objects.filter(Brand='ACNE')
        product = Product.objects.get(id=prod_id)
        reviews = ReviewRating.objects.filter(Q(product_id=product.id, status=True))
        product = Product.objects.get(id=prod_id)
        sideofferbar = Sideofferbar.objects.all()
        item_already_in_cart = False
        review = ReviewRating.objects.filter(product_id=product.id).count()
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(user=customer, complete=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            cookieData = cookieCart(request)
            cartItems = cookieData['cartItems']
            order = cookieData['order']
            items = cookieData['items']
        return render(request, 'product-details.html',
                      {'product': product, 'item_already_in_cart': item_already_in_cart,
                       'details': details, 'recommended': recommended, 'fendi': fendi, 'albiro': albiro, 'gucci': gucci,
                       'chanel': chanel, 'prada': prada, 'underarmour': underarmour, 'acne': acne,
                       'recommended1': recommended1, 'kids': kids, 'reviews': reviews, 'review': review,
                       'sideofferbar': sideofferbar, 'cartItems': cartItems, 'items': items})

    '''
def product_details(request):
    return render(request, 'product-details.html', {})
'''


# @method_decorator(login_required, name='dispatch')
class CheckoutnewView(View):
    def post(self, request):
        global cartItems, add
        if request.user.is_authenticated:
            try:
                customer = request.user
                order, created = Order.objects.get_or_create(user=customer, complete=False)
                items = order.orderitem_set.all()
                cartItems = order.get_cart_items
                add = ()
            except:
                print('hello')

        else:
            data = cartData(request)
            cartItems = data['cartItems']
            order = data['order']
            items = data['items']
            add = ()
        return render(request, 'store/checkoutnew.html', {'items': items,
                                                          'order': order, 'cartItems': cartItems, 'add': add})

    def get(self, request):
        global cartItems, add
        if request.user.is_authenticated:
            try:
                user = request.user
                add = Customer.objects.filter(user=user)
                data = cartData(request)
                cartItems = data['cartItems']
                order = data['order']
                items = data['items']
                print('try')
            except:
                print('hello')

        else:
            data = cartData(request)
            cartItems = data['cartItems']
            order = data['order']
            items = data['items']
            add = ()
        return render(request, 'store/checkoutnew.html', {'items': items,
                                                          'order': order, 'cartItems': cartItems, 'add': add})


def cartnew(request):
    global order, cartItems, cart

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        if cartItems == 0:
            return render(request, 'emptycart.html', {'None': None})
        else:
            pass
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        if cartItems == 0:
            return render(request, 'emptycart.html', {'None': None})
        else:
            pass

    return render(request, 'store/cartnew.html', {'items': items, 'order': order, 'cartItems': cartItems})


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(user=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)


@login_required
def add_to_cart(request):
    if request.user.is_authenticated:
        user = request.user
        print("user")
        # product_id = request.GET.get('prod_id')
        #   print("prod_id",product_id)
        product = Product.objects.get(id=1)
        print("int")
        Cart(user=user, product=product).save()
        return redirect('/cart/')
    if not request.user.is_authenticated:
        try:
            user = request.user
        except:
            device = request.COOKIES['device']
            user, created = User.objects.get_or_create(device=device)

        created = Product.objects.get_or_create(cart=user)

        context = {'created': created}
        return render(request, 'store/cart.html', context)


def show_cart(request):
    global totalamount, tamount, totalitem, cart
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        user = request.user
        cart = Cart.objects.filter(user=user)
        print(cart)
        amount = 0.0
        shipping_amount = 2.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
                tamount = (p.quantity * p.product.discounted_price)
            return render(request, 'cart.html', {'carts': cart, 'totalamount': totalamount,
                                                 'totalitem': totalitem, 'amount': amount,
                                                 'tamount': tamount})
        else:
            return render(request, 'emptycart.html')

    if not request.user.is_authenticated:
        # totalitem = len(Cart.objects.filter(user=request.user))
        user = request.session['cartdata']
        request.session['cartdata'] = cart_data
        cart_data[str(request.GET['id'])]['qty'] = int(cart_p[str(request.GET['id'])]['qty'])
        # cart = Cart.objects.filter(user=user)
        # print(cart)
        amount = 0.0
        shipping_amount = 2.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        print(cart_product)

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamount = amount + shipping_amount
                tamount = (p.quantity * p.product.discounted_price)
            return render(request, 'cart.html', {'carts': cart, 'totalamount': totalamount,
                                                 'totalitem': totalitem, 'amount': amount,
                                                 'tamount': tamount})
        else:
            return render(request, 'emptycart.html')


def plus_cart(request):
    global totalamount
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) &
                             Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 2.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

        data = {

            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount

        }
        return JsonResponse(data)


def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        # print(prod_id)
        c = Cart.objects.get(Q(product=prod_id) &
                             Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 2.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount + shipping_amount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        print("success2")
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) &
                             Q(user=request.user))
        c.delete()
        print("success1")
        amount = 0.0
        shipping_amount = 2.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]

        for p in cart_product:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
            # totalamount = amount

        data = {

            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount + shipping_amount
        }
        print("success")
        return JsonResponse(data)


def Pagenotfound(request):
    return render(request, '404.html', {})


def womens(request, data=None):
    global womens, mens
    # values = ["blue", "green", "brown"]
    # context = {'count': Product.objects.count()}
    if data == None:
        womens = Product.objects.filter(category='WOMENS')
    elif data == 'FENDI' or data == 'GUESS':
        womens = Product.objects.filter(category='WOMENS').filter(Brand=data)
    elif data == 'NIKE':
        womens = Product.objects.filter(Brand=data)
    elif data == 'UNDERARMOUR':
        womens = Product.objects.filter(Brand=data)
    elif data == 'ACNE' or 'ALBIRO':
        womens = Product.objects.filter(Brand=data)
    elif data == 'Kids':
        womens = Product.objects.filter(category='KIDS')
    elif data == 'below':
        womens = Product.objects.filter(category='WOMENS').filter(discounted_price__lt=25)
    elif data == 'above':
        womens = Product.objects.filter(category='WOMENS').filter(discounted_price__gt=32)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return render(request, 'womens.html', {'womens': womens, 'items': items,
                                           'cartItems': cartItems, 'count': Product.objects.count()})


def mens(request, data=None):
    global mens
    if data == None:
        mens = Product.objects.filter(category='MENS')
    elif data == 'FENDI' or 'GUESS':
        mens = Product.objects.filter(category='MENS').filter(Brand=data)
    elif data == 'VALENTINO' or 'DIOR':
        mens = Product.objects.filter(category='MENS').filter(Brand=data)
    elif data == 'ARMANI' or 'PRADA':
        mens = Product.objects.filter(category='MENS').filter(Brand=data)
    elif data == 'CHANEL' or 'GUCCI':
        mens = Product.objects.filter(category='MENS').filter(Brand=data)
    elif data == 'VALENTINO' or data == 'DIOR':
        mens = Product.objects.filter(category='MENS').filter(Brand=data)
    return render(request, 'mens.html', {'mens': mens})


def filter_data(request):
    minPrice = request.GET['minPrice']
    maxPrice = request.GET['maxPrice']
    allProducts = Product.objects.all().order_by('-id').distinct()
    allProducts = Products.objects.filter(discounted_price__gte=minPrice)
    allProducts = Products.objects.filter(discounted_price__lte=maxPrice)
    t = render_to_string('mens.html', {'data': allProducts})
    return JsonResponse({'data': t})


'''
''
global topwears
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Lewis' or data == 'PeterEngland':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=300)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=400)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/topwear.html', {'topwears': topwears, 'totalitem
'''


def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)


def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(pk=pid)
    data = {}
    checkw = Wishlist.objects.filter(product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


# My Wishlist
def my_wishlist(request):
    wlist = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'wishlist.html', {'wlist': wlist})


def address(request):
    global totalitem
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'address.html', {'add': add, 'totalitem': totalitem})


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        global totalitem
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'profile.html', {'form': form, 'totalitem': totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=user, name=name, locality=locality, city=city,
                           state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Profile updates Successfully')
        return render(request, 'profile.html', {'form': form})


def search(request):
    global query
    query = request.GET['query']
    feature_item = Product.objects.filter(product_name__icontains=query)
    context = {
        'feature_item': feature_item
    }
    return render(request, 'search.html', context)


def processOrder(request):
    global user
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)

        if order.shipping == True:
            Customer.objects.create(
                user=user,
                order=order,
                locality=data['shipping']['locality'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        Customer.objects.create(
            user=user,
            order=order,
            locality=data['shipping']['locality'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment submitted..', safe=False)
