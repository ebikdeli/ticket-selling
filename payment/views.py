from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Payment
from order.models import Order



@login_required
def payment_success(request):
    """Redirect user to this page if payment was successful"""
    latest_order_qs = Order.objects.filter(user=request.user, is_paid=True, is_active=True)
    if latest_order_qs.exists():
        latest_order = latest_order_qs.first()
    else:
        return redirect(reverse('vitrin:index'))
    # Make current order in_active
    latest_order.is_active = False
    latest_order.save()
    # If payment is successful update the payment object
    payment_qs = Payment.objects.filter(user=request.user, order=latest_order)
    if payment_qs.exists():
        payment = payment_qs.get()
        payment.is_paid = True
        payment.save()
    # remove Tickets and Ticketsolds from the cart
    cart = latest_order.cart
    for ts in cart.ticketsold_cart.all():
        if not ts.is_paid:
            ts.is_paid = True
            ts.is_active = False
            ts.save()
            cart.ticketsold_cart.remove(ts)
            cart.ticket.remove(ts.ticket)
    cart.is_paid = False
    cart.save()
    return render(request, 'payment/payment-success.html', {'order': latest_order})


@login_required
def payment_failed(request):
    """Redirect user to this page if payment was a failure"""
    return render(request, 'payment/payment-failed.html')


@login_required
def payment_request(request, order_id=None):
    """Payment request for user to pay for the order"""
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return reverse('dashboard:dashboard')
    order = order_qs.get()
    # Create payment object for before order being paid
    payment = Payment.objects.create(user=request.user,
                                    order=order,
                                    price=order.total_price,
                                    describtion='خرید بلیط ترندویل',
                                    pgi='zarrin')
    context = {'order': order}
    return render(request, 'payment/payment-request.html', context=context)


@login_required
def zarrin_pal_request(request, order_id=None):
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return reverse('dashboard:dashboard')
    order = order_qs.get()
    """If user select zarrin-pal pgi redirected here"""
    return JsonResponse(data={'msg': 'درگاه زرین پال انتخاب شده', 'order-id': order.order_id})


@login_required
def next_pay_request(request, order_id=None):
    """If user select next-pay pgi redirected here"""
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return reverse('dashboard:dashboard')
    order = order_qs.get()
    return JsonResponse(data={'msg': 'درگاه نکست پی انتخاب شده', 'order-id': order.order_id})
