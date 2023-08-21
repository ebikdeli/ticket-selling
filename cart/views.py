"""
All views created to work with Ajax calls
"""
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Cart
from ticket.models import Ticket, TicketSold
import json


def cart_view(request):
    """View current active cart for the user"""
    # For authenticated users, if cart is empty, delete all active order (if any exist)
    # if request.user.is_authenticated:
    #     cart = request.user.cart_user.first()
    #     if not cart.total_quantity:
    #         cart.order_cart.filter(is_active=True).delete()
    return render(request, 'cart/cart.html')


def add_ticket_cart(request):
    """Add ticket to cart"""
    if request.method == 'POST':
        # * Process received data and check if there is no error
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        ticket_id = data.get('ticket-id', None)
        quantity = data.get('quantity', None)
        cart_id = data.get('cart-id', None)
        if not ticket_id or not quantity:
            return JsonResponse(data={'msg': 'دیتای ارسالی فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        ticket_qs = Ticket.objects.filter(id=ticket_id)
        if not ticket_qs.exists():
            return JsonResponse(data={'msg': 'بلیطی با مشخصه ارسالی دریافت نشد', 'code': 402, 'status': 'nok'})
        # * Put ticket into the cart
        # Get current Cart
        if not cart_id:
            if request.user.is_authenticated:
                cart_id = request.user.cart_user.first().id
            else:
                try:
                    cart_id = request.session['cart_id']
                except KeyError:
                    return JsonResponse({'msg': 'سرور در حال حاضر مشکل دارد', 'code': 402, 'status': 'nok'})
        cart_qs = Cart.objects.filter(id=cart_id)
        if not cart_qs.exists():
            return JsonResponse(data={'msg': 'ارتباط با سبد خرید برقرار نشد', 'code': 402, 'status': 'nok'})
        cart = cart_qs.get()
        ticket = ticket_qs.get()
        # *** Following method append ticket to the user cart
        result = cart.append_ticket(request, quantity, ticket)
        if not result:
            return JsonResponse(data={'msg': 'مشکلی پیش آمده و محصول در سبد خرید ثبت نشد', 'code': 402, 'status': 'nok'})
        # Item successfully added to cart
        return JsonResponse(data={'msg': 'محصول در سبد خرید قرار گرفت', 'code': 201, 'status': 'ok'})
    # If any method except of the 'POST' come, send following message
    return JsonResponse(data={'msg': 'bad request method', 'code': 400, 'status': 'nok'})


def change_ticket_cart(request):
    """Change number of items in the cart"""
    if request.method == 'POST':
        # * Process received data and check if there is no error
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        # get product to be changed on quantity
        # ticketsold_id = data.get('ticketsold-id', None)
        ticket_id = data.get('ticket-id', None)
        quantity = data.get('quantity', None)
        cart_id = data.get('cart-id', None)
        # if not ticketsold_id or not quantity:
        if not ticket_id or not quantity:
            return JsonResponse(data={'msg': 'دیتای ارسالی فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        # ticketsold_qs = TicketSold.objects.filter(id=ticketsold_id)
        ticket_qs = Ticket.objects.filter(id=ticket_id)
        # if not ticketsold_qs.exists():
        if not ticket_qs.exists():
            return JsonResponse(data={'msg': 'بلیطی با مشخصه ارسالی خریداری نشده', 'code': 402, 'status': 'nok'})
        # * update ticket into the cart
        # Get current Cart
        if not cart_id:
            if request.user.is_authenticated:
                cart_id = request.user.cart_user.first().id
            else:
                try:
                    cart_id = request.session['cart_id']
                except KeyError:
                    return JsonResponse({'msg': 'سرور در حال حاضر مشکل دارد', 'code': 402, 'status': 'nok'})
        cart_qs = Cart.objects.filter(id=cart_id)
        if not cart_qs.exists():
            return JsonResponse(data={'msg': 'ارتباط با سبد خرید برقرار نشد', 'code': 402, 'status': 'nok'})
        cart = cart_qs.get()
        # ticketsold = ticketsold_qs.get()
        ticket = ticket_qs.get()
        ticketsold_qs = TicketSold.objects.filter(ticket=ticket, cart=cart)
        if not ticketsold_qs.exists():
            return JsonResponse({'msg': 'سرور در پردازش سبد خرید و بلیط خریداری شده مشکل دارد', 'code': 402, 'status': 'nok'})
        ticketsold = ticketsold_qs.get()
        # *** Following method append ticket to the user cart
        result = cart.change_ticket_quantity(request, quantity, ticketsold)
        if not result:
            return JsonResponse(data={'msg': 'مشکلی پیش آمده و تعداد بلیط ها افزایش نیافت', 'code': 402, 'status': 'nok'})
        # Item successfully added to cart
        return JsonResponse(data={'msg': 'عملیات تغییر تعداد بلیط با موفقیت انجام گرفت', 'code': 201, 'status': 'ok'})
    # If any method except of the 'POST' come, send following message
    return JsonResponse(data={'msg': 'bad request method', 'code': 400, 'status': 'nok'})


def delete_ticket_cart(request):
    """"Delete selected ticketsold from the cart"""
    if request.method == 'POST':
        # * Process POST data
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'هیچ دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        ticket_id = data.get('ticket-id', None)
        cart_id = data.get('cart-id', None)
        # if not ticketsold_id or not quantity:
        if not ticket_id:
            return JsonResponse(data={'msg': 'دیتای دریافتی فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        # get the cart that ticket should get deleted from
        if not cart_id:
            if request.user.is_authenticated:
                cart_id = request.user.cart_user.first().id
            else:
                try:
                    cart_id = request.session['cart_id']
                except KeyError:
                    return JsonResponse({'msg': 'سرور در حال حاضر مشکل دارد', 'code': 402, 'status': 'nok'})
        cart_qs = Cart.objects.filter(id=cart_id)
        if not cart_qs.exists():
            return JsonResponse(data={'msg': 'سبد خرید انتخاب شده فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        cart = cart_qs.get()
        # get product to be deleted
        # ticketsold_qs = TicketSold.objects.filter(id=ticketsold_id)
        ticket_qs = Ticket.objects.filter(id=ticket_id)
        # if not ticketsold_qs.exists():
        if not ticket_qs.exists():
            return JsonResponse(data={'msg': 'کد بلیط انتخاب شده اشتباه است', 'code': 402, 'status': 'nok'})
        # ticketsold = ticketsold_qs.get()
        ticket = ticket_qs.get()
        ticketsold_qs = TicketSold.objects.filter(ticket=ticket, cart=cart)
        if not ticketsold_qs.exists():
            return JsonResponse({'msg': 'سرور در پردازش سبد خرید و بلیط خریداری شده مشکل دارد', 'code': 402, 'status': 'nok'})
        ticketsold = ticketsold_qs.get()
        # get ticketsold
        # Delete ticket from the cart
        result = cart.delete_item(request, ticketsold)
        # If there is a problem notify the customer
        if not result:
            return JsonResponse(data={'msg': 'مشکلی پیش آمده و بلیط از سبد خرید حذف نشد', 'code': 402, 'status': 'nok'})
        # If ticket successfully deleted from the cart, notify the customer
        return JsonResponse(data={'msg': 'بلیط با موفقیت از سبد خرید حذ شد', 'code': 202, 'status': 'ok'})
    return JsonResponse(data={'msg': 'متد اشتباه است', 'code': 400, 'status': 'nok'})


def clean_cart(request):
    """Clean cart totally"""
    if request.method == 'POST':
        # * Process POST data
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'هیچ دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        cart_id = data.get('cart-id', None)
        if not cart_id:
            if request.user.is_authenticated:
                cart_id = request.user.cart_user.first().id
            else:
                try:
                    cart_id = request.session['cart_id']
                except KeyError:
                    return JsonResponse({'msg': 'سرور در حال حاضر مشکل دارد', 'code': 402, 'status': 'nok'})
        cart_qs = Cart.objects.filter(id=cart_id)
        if not cart_qs.exists():
            return JsonResponse(data={'msg': 'سبد خرید انتخاب شده فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        cart = cart_qs.get()
        result = cart.clear(request)
        if not result:
            return JsonResponse(data={'msg': 'مشکلی پیش آمده و سبد خرید خالی نشد', 'code': 402, 'status': 'nok'})
        # If cart successfully cleaned, notify the customer
        return JsonResponse(data={'msg': 'سبد خرید با موفقیت تخلیه شد', 'code': 202, 'status': 'ok'})
    return JsonResponse(data={'msg': 'متد اشتباه است', 'code': 400, 'status': 'nok'})
