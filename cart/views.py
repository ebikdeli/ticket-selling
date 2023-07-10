from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse
from .models import Cart
import json


def cart_view(request):
    return render(request, 'cart/templates/cart/cart_view.html')


def add_product_cart(request):
    """Add item to cart"""
    if request.method == 'POST':
        # * Process received data and check if there is no error
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        product_id = data.get('product-id', None)
        color_name = data.get('color', None)
        quantity = data.get('quantity', None)
        if not product_id:
            return JsonResponse(data={'msg': 'دیتای ارسالی فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        product_qs = Product.objects.filter(product_id=product_id)
        if not product_qs.exists():
            return JsonResponse(data={'msg': 'محصولی با مشخصه ارسالی یافت نشد', 'code': 402, 'status': 'nok'})
        # * Put product into the cart
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
        product = product_qs.get()
        result = cart.append_item(request, quantity, product_id, color_name)
        if not result:
            return JsonResponse(data={'msg': 'مشکلی پیش آمده و محصول در سبد خرید ثبت نشد', 'code': 402, 'status': 'nok'})
        # Item successfully added to cart
        return JsonResponse(data={'msg': 'محصول در سبد خرید قرار گرفت', 'code': 201, 'status': 'ok'})
    # If any method except of the 'POST' come, send following message
    return JsonResponse(data={'msg': 'bad request method', 'code': 400, 'status': 'nok'})


def change_product_cart(request):
    """Change number of items in the cart"""
    if request.method == 'POST':
        # * Process POST data
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'هیچ دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        product_id = data.get('product-id', None)
        cart_id = data.get('cart-id', None)
        quantity = data.get('quantity', None)
        if not product_id:
            return JsonResponse(data={'msg': 'دیتای ارسالی فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        product_qs = Product.objects.filter(product_id=product_id)
        if not product_qs.exists():
            return JsonResponse(data={'msg': 'محصولی با مشخصه ارسالی یافت نشد', 'code': 402, 'status': 'nok'})
        # * Put product into the cart
        if not cart_id:
            return JsonResponse({'msg': 'سرور در حال حاضر مشکل دارد', 'code': 402, 'status': 'nok'})
        cart_qs = Cart.objects.filter(id=cart_id)
        if not cart_qs.exists():
            return JsonResponse(data={'msg': 'ارتباط با سبد خرید برقرار نشد', 'code': 402, 'status': 'nok'})
        cart = cart_qs.get()
        product = product_qs.get()
        # Get current CartItem
        cart_item_qs = cart.cart_item_cart.filter(product=product)
        if not cart_item_qs.exists():
            return JsonResponse({'msg': 'آیتم مورد نظر پیدا نشد', 'code': 402, 'status': 'nok'})
        cart_item = cart_item_qs.get()
        result = cart.change_item_quantity(quantity, request, cart_item)
        if not result:
            return JsonResponse(data={'msg': 'عملیات تغییر محصول با مشکل مواجه شد', 'code': 402, 'status': 'nok'})
        # If there is no error in the request return success message
        return JsonResponse(data={'msg': 'تغییر تعداد محصول با موفقیت انجام شد', 'code': 201, 'status': 'ok'})
    # If any method called except for POST, return following code
    return JsonResponse(data={'msg': 'متد اشتباه است', 'code': 400, 'status': 'nok'})


def delete_item_cart(request):
    """"Delete selected item from the cart"""
    if request.method == 'POST':
        # * Process POST data
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'هیچ دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        product_id = data.get('product-id', None)
        cart_id = data.get('cart-id', None)
        if not product_id or not cart_id:
            return JsonResponse(data={'msg': 'دیتای دریافتی فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        # get product to be deleted
        product_qs = Product.objects.filter(product_id=product_id)
        if not product_qs.exists():
            return JsonResponse(data={'msg': 'کد محصول انتخاب شده اشتباه است', 'code': 402, 'status': 'nok'})
        product = product_qs.get()
        # get the cart that product should get deleted from
        cart_qs = Cart.objects.filter(id=cart_id)
        if not cart_qs.exists():
            return JsonResponse(data={'msg': 'سبد خرید انتخاب شده فاقد اعتبار است', 'code': 402, 'status': 'nok'})
        cart = cart_qs.get()
        # get CartItem
        cart_item_qs = cart.cart_item_cart.filter(product=product)
        if not cart_item_qs.exists():
            return JsonResponse(data={'msg': 'آیتم مورد نظر در سبد خرید پیدا نشد', 'code': 402, 'status': 'nok'})
        cart_item = cart_item_qs.get()
        # Delete item from the cart
        result = cart.delete_item(request, cart_item, product)
        # If there is a problem notify the customer
        if not result:
            return JsonResponse(data={'msg': 'مشکلی پیش آمده و آیتم از سبد خرید حذف نشد', 'code': 402, 'status': 'nok'})
        # If item successfully deleted from the cart, notify the customer
        return JsonResponse(data={'msg': 'آیتم با موفقیت از سبد خرید حذ شد', 'code': 202, 'status': 'ok'})
    return JsonResponse(data={'msg': 'متد اشتباه است', 'code': 400, 'status': 'nok'})
