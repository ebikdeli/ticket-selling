from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Order
from .forms import OrderForm


@login_required
def order_form(request):
    """Before order created, the customer must fill a form to verify his/her address
    NOTE: user most be login"""
    # Get latest user 'address' and 'cart'
    address = request.user.address_user.first() if request.user.address_user.exists() else None
    cart = request.user.cart_user.first()
    if not cart:
        return redirect(reverse('vitrin:index'))
    # if cart.quantity <= 1:
    #     return redirect(reverse('vitrin:index'))
    # # ? Check if current 'cart' has any active order
    # order_qs = cart.order_cart.filter(is_active=True, is_paid=False)
    # if order_qs.exists():
    #     return redirect(reverse('vitrin:index'))
    # # If method is POST process order-form and create a new Order for the user
    if request.method == 'POST':
        # We can also use 'cart_id' session to get current Cart
        order_form = OrderForm(data=request.POST)
        if order_form.is_valid():
            data = order_form.cleaned_data
            order = cart.order_cart.create()
            # update 'user' and 'address'
            user = request.user
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.phone = data['phone']
            user.email = data['email']
            user.save()
            new_address = request.user.address_user.create(
                postal=data['postal'],
                state=data['state'],
                city=data['city'],
                line=data['line'],
                phone=user.phone
            )
            print(new_address)
            return redirect(reverse('order:checkout', kwargs={'order_id': order.order_id}))
        else:
            print(order_form.errors)
    # When method is GET tell the user to fill 'order-form' before creation of order
    context = {'address': address}
    return render(request, 'order/order-form.html', context)


@login_required
def checkout(request):
    """Order checkout for current Cart"""
    cart = request.user.cart_user.first()
    # If cart is empty, delete all active order (if any exist)
    if not cart.total_quantity:
        cart.order_cart.filter(is_active=True).delete()
        return redirect('cart:cart-view')
    if not cart.order_cart.exists():
        print('NEW ORDER CREATED')
        order = cart.order_cart.create(user=request.user)
    else:
        print('ORDER ALREADY EXISTS')
        order = cart.order_cart.filter(is_active=True).first()
    context = {'order': order}
    return render(request, 'order/checkout.html', context=context)


@login_required
def order_detail(request, order_id=None):
    """View details of the order"""
    # 'order_found=-1' means there is no such an order. 'order_found=0' means order is registered but no item in it. 'order_found=1' means order is registered with item in it
    order = Order.objects.filter(order_id=order_id).get() if Order.objects.filter(order_id=order_id).exists() else None
    if not order:
        print('THIS ORDER IS NOT REGISTERED')
    else:
        print('THIS ORDER HAS BEEN REGISTERED')
    context = {'order': order}
    return render(request, 'order/order-detail.html', context=context)



@login_required
def my_tickets(request):
    """Return list of all of the tickets bought by user in history"""
    pass