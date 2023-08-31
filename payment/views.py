from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import JsonResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Payment
from . import pgi
from order.models import Order
from urllib.parse import unquote



@login_required
def zarrinpal_request(request, order_id:str):
    """Start payment request for user to pay for the order. If payment data verified by zarrin-pal, redirect user to the zarrin pgi"""
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return redirect('dashboard:profile')
    order = order_qs.get()
    # Create payment object for before order being paid
    payment = Payment.objects.create(user=request.user,
                                    order=order,
                                    price=order.total_price,
                                    describtion='خرید بلیط ترندویل',
                                    pgi='zarrin')
    result = pgi.zarin_initialize_payment(request, order, payment)
    # If payment request has error in it, redirect user to the payment_failed page
    if result['status'] == 'error':
        return redirect('payment:payment-failed', order_id=order_id, message=result['message'])
    zarrin_pgi_url = result['data']
    return redirect(zarrin_pgi_url)
    


@login_required
def zarrinpal_result_redirect(request, order_id:str, payment_id:str):
    """This is the view for callback url in zarrin pal. This view executed after user interacted with zarrin PGI."""
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return redirect('vitrin:index')
    payment_qs = Payment.objects.filter(id=payment_id)
    if not payment_qs.exists():
        return redirect('vitrin:index')
    order = order_qs.get()
    payment = payment_qs.get()
    payment_status = request.GET.get('Status', None)
    payment_authority = request.GET.get('Authority', None)
    if not payment_status or not payment_authority:
        return redirect('vitrin:index')
    result = pgi.zarin_payment_result_verify(request, order)
    # If payment was a failure redirect user to 'payment-failed' view
    if result['status'] == 'error':
        return redirect('payment:payment-failed', order_id=order_id, message=result['message'])
    # If payment was a success, change order and payment status to True and redirect them to payment_success
    order.is_paid = True
    order.is_active = False
    order.authority = payment_authority
    order.save()
    payment.is_paid = True
    payment.save()
    return redirect('payment: payment_success', order_id=order_id)


@login_required
def payment_success(request, order_id:str):
    """Redirect user to this page if payment was successful"""
    # latest_order_qs = Order.objects.filter(user=request.user, is_paid=True, is_active=True)
    latest_order_qs = Order.objects.filter(order_id=order_id, is_paid=True, is_active=False)
    if latest_order_qs.exists():
        latest_order = latest_order_qs.first()
    else:
        return redirect(reverse('vitrin:index'))
    # Make current order deactive
    latest_order.is_paid = True
    latest_order.is_active = False
    latest_order.save()
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
def payment_failed(request, order_id:str, message:str):
    """Redirect user to this page if payment was a failure"""
    order_qs = Order.objects.filter(order_id=order_id)
    if not order_qs.exists():
        return redirect('vitrin:index')
    order = order_qs.get()
    unquoted_message = unquote(message)
    context = {'order': order, 'message': unquoted_message}
    return render(request, 'payment/payment-failed.html', context)
