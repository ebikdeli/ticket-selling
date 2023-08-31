"""
** I think in client-server architecture it is better to let client to handle payment procedure but for now Arash does
not have the expertise to do that.

** Because HTTP HEADERS do not accept 'non-ascii' characters, we define equall 'ascii' response for every 'non-ascii'
'non-ascii' response! Look at 'error' data in this module.

** This code writen for ZarinPal pgi, but we can use it for any REST pgi service with minimal changes.
Note: Using 'global variables' increases the risk of process race between users and expose a user data
to other users. So it's not recommmended.
It's important to remember we cannot use 'sessions' to pass data between diffrent views
because the 'pgi' does not use the same session as user and we can't pass data between 2 diffrent sessions.
In 2 ways we can solve this issue: 1- Using 'variables' in the view's 'url' to send unique data (eg:username)
to the  2- Use additional headers or variables in token based
authentication.

** Note that we should not use 'redirect' function in helper modules. Else we get ValueError None type object error.

** https://docs.djangoproject.com/en/4.0/ref/request-response/#django.http.HttpRequest.get_host
"""
from django.conf import settings
from django.urls import reverse
import requests
import json



def zarin_initialize_payment(request, order:object, payment:object) -> dict:
    """Initialize payment process and redirect user to pgi in Zarrin Pal. Return result as a dict"""
    try:
        location = reverse('payment:zarrinpal_result_redirect', kwargs={'order_id': order.order_id, 'payment_id': payment.id})
        callback_url = f'{request.scheme}://{request.get_host()}{location}'
        url = 'https://api.zarinpal.com/pg/v4/payment/request.json'
        headers = {'accept': 'application/json',
                'content-type': 'application/json'}
        data = {
            'merchant_id': settings.ZARIN_MERCHANT_ID,
            # 'amount': int(order.total_price) * 10,
            'amount': 1000,
            'description': f'پرداخت برای بلیط در ترندویل',
            'callback_url': callback_url,
            'metadata': {'email': request.user.email,
                        'phone': request.user.phone}
                        }
        try:
            r = requests.post(url=url, data=json.dumps(data), headers=headers)
        except (requests.ConnectionError, requests.ReadTimeout, requests.RequestException):
            result = {'status': 'error', 'message': 'برقراری ارتباط با واسط پرداخت به مشکل برخورده', 'data': None}
            return result
        if r.status_code == 200 or 201:
            zarin_response = r.json()
            # If request for payment was a success:
            if zarin_response['data']:
                authority = zarin_response['data']['authority']
                zarrin_pgi_url = f'https://www.zarinpal.com/pg/StartPay/{authority}'
                # Redirect user to PGI to pay
                result = {'status': 'ok',
                    'message': 'احراز هویت پذیرنده و اطلاعات پرداخت با موفقیت صورت پذیرفت. مشتری باید به درگاه پرداخت هدایت شود',
                    'data': zarrin_pgi_url}
                return result
            # If there is a error:
            else:
                error = _zarin_error_decode(zarin_response)
                result = {'status': 'error', 'message': error, 'data': None}
                return result
        else:
            result = {'status': 'error', 'message': 'ارتباط با سایت پذیرنده ممکن نمی باشد', 'data': None}
            return result
    except Exception as e:
        data={'status': 'error', 'message': 'مشکلی در برنامه پیش آمده و پرداخت انجام نمی گیرد', 'data': None}
        return data


def zarin_payment_result_verify(request, order:object):
    """Used in the last step to verify the payment then redirect user to receipt"""
    try:
        payment_status = request.GET.get('Status', None)
        payment_authority = request.GET.get('Authority', None)
        url = 'https://api.zarinpal.com/pg/v4/payment/verify.json'
        data = {
            'merchant_id': settings.ZARIN_MERCHANT_ID,
            # 'amount': int(order.total_price) * 10,
            'amount': 1000,
            'authority': payment_authority
                }
        headers = {'accept': 'application/json',
                'content-type': 'application/json'}
        try:
            r = requests.post(url=url, data=json.dumps(data), headers=headers)
        except (requests.ConnectionError, requests.ReadTimeout, requests.RequestException):
            data={'status': 'error', 'message': 'برقراری ارتباط با واسط پرداخت به مشکل برخورده', 'data': None}
            return data
        if r.status_code == 200 or 201:
            zarin_response = r.json()
            # If payment was a success execute following block
            if zarin_response['data'] and payment_status == 'OK':
                result = {'status': 'ok', 'message': 'سفارش شما با موفقیت ثبت شد', 'data': 1}
                return result
            # If there is an error in the payment execute following block
            else:
                error = _zarin_error_decode(zarin_response)
                data={'status': 'error', 'message': error, 'data': None}
                return data
    except Exception as e:
        data={'status': 'error', 'message': 'مشکلی در برنامه پیش آمده و پرداخت انجام نمی گیرد', 'data': None}
        return data


def _zarin_error_decode(zarin_response) -> str:
    """Helper function to decode error message in payment process. Return a string represents the error message"""
    code = zarin_response['errors']['code']
    if code == -9:
        error = 'کد پذیرنده اشتباه یا مبلغ پرداختی کمتر از 1000 ریال است'
        # error = 'Less than 1000 Rials in your account'
    if code == -10:
        error = 'آدرس آی پی یا مرچنت کد پذیرنده صحیح نیست'
        # error = 'IP address or Merchant code of Accepter is not valid'
    if code == -11:
        error = 'کد پذیرنده فعال نیست'
    if code == -12:
        error = 'تلاش بیش از اندازه در یک بازه زمانی کوتاه. بعدا تلاش کنید'
        # error = 'Too many request in short time period. Try later'
    if code == -34:
        error =  'مبلغ وارد شده از تراکنش بیشتر است'
        # error = 'Input money is more than transaction'
    if code == -36:
        error = 'موجودی باید بیش از 1000 ریال باشد'
    if code == -51:
        error = 'انصراف از پرداخت'
        # error = 'پرداخت ناموفق. از پرداخت منصرف شده اید'
        # error = 'You Have cancelled the payment'
    if code == -53:
        error = 'کد اتوریتی نامعتبر است'
        # error = 'Authority code is invalid'
    # return {'code': code, 'error': error}
    return error