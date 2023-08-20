from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Order


@login_required
def order(request):
    """Show active order that is in the current cart. Everytime user come to this page, every other unpaid orders deleted and a new order created for the user"""
    # Get latest user 'address' and 'cart'
    cart = request.user.cart_user.first()
    if not cart.total_quantity:
        return redirect(reverse('vitrin:index'))
    order_qs = cart.order_cart.filter(is_active=True, is_paid=False)
    for order in order_qs:
        order.delete()
    order = cart.order_cart.create(user=request.user)
    context = {'order': order}
    return render(request, 'order/order.html', context)


@login_required
def order_detail(request, order_id=None):
    """View details of the order"""
    # 'order_found=-1' means there is no such an order. 'order_found=0' means order is registered but no item in it. 'order_found=1' means order is registered with item in it
    order = Order.objects.filter(order_id=order_id).get() if Order.objects.filter(order_id=order_id).exists() else None
    if not order:
        return redirect(reverse('vitrin:index'))
    context = {'order': order}
    return render(request, 'order/order-detail.html', context=context)



@login_required
def my_tickets(request):
    """Return list of all of the ticketsolds bought by user in history"""
    bought_ticketsolds = []
    orders = Order.objects.filter(user=request.user, is_paid=True)
    if orders.exists():
        for order in orders:
            for ts in order.tickets:
                bought_ticketsolds.append(ts)
    context = {'bought_ticketsolds': bought_ticketsolds}
    return render(request, 'order/my-tickets.html', context)
