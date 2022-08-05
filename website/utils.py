import json
from .models import *


def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('Cart:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            cartItems += cart[i]["quantity"]
            # print("for",i)

            product1 = Product.objects.get(id=i)

            # print("h", id)
            total = (product1.discounted_price * cart[i]["quantity"])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]["quantity"]

            item = {
                'product': {
                    'id': product1.id,
                    'product_name': product1.product_name,
                    'discounted_price': product1.discounted_price,
                    'prod_image': product1.prod_image,
                },
                'quantity': cart[i]["quantity"],
                'get_total': total
            }
            items.append(item)

        except:

            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}


def cartData(request):
    global cartItems
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

    return {'cartItems': cartItems, 'order': order, 'items': items}

def guestOrder(request, data):
    print('USer is not logged in....')

    print('COOKIES:', request.COOKIES)
    user = data['form']['user']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(
        user=user
    )
    customer.user = user
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False,
    )

    for item in items:
        product = Product.objects.get(id - item['product']['id'])

        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )

    return order, customer