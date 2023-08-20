# ! Data Validation should be happened in front-end
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
# from django.views.decorators.cache import cache_page, never_cache
from cart.models import Cart
from .forms import UserPasswordChangeForm
from .login import user_signup_login, user_password_change
import json


def login_signup(request):
    """login and signup page form integrated into single page. All form validation happening in front-end"""
    return render(request, 'login/login-signup.html')


# @cache_page(60 * 15)
def classic_login(request):
    """Handles the classic or ordinary user login procedure"""
    if request.method == 'POST':
        data_json = request.POST['data']
        if not data_json:
            return JsonResponse(data={'msg': 'اطلاعاتی دریافت نشد', 'status': 'nok', 'code': 400})
        data = json.loads(data_json)
        username = data.get('username', None)
        if not username:
            return JsonResponse(data={'msg': 'ایمیل دریافت نشد', 'status': 'nok', 'code': 409})
        password = data.get('password', None)
        if not password:
            return JsonResponse(data={'msg': 'رمز عبور دریافت نشد', 'status': 'nok', 'code': 410})
        user = authenticate(request,
                            username=username,
                            password=password)
        if user:
            login(request, user)
            cart = user.cart_user.first()
            # Synchronize Cart data with cart session data after login
            cart.sync_session_cart_after_authentication(request)
            return JsonResponse(data={'msg': 'ورود با موفقیت انجام گرفت', 'status': 'ok', 'code': 200})
        else:
            return JsonResponse(data={'msg': 'نام کاربری یا رمز عبور اشتباه است', 'status': 'nok','code': 401})
    else:
        return render(request, 'login/signin.html')


@login_required
def logout_view(request):
    """Logout user from website"""
    logout(request)
    messages.success(request, _('You have logout of your user account'))
    return redirect('vitrin:index')


# @cache_page(60 * 15)
def signup(request):
    """SignUp user after user proceeds with signup form in 'user_signup_view"""
    if request.method == 'POST':
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'داده ای دریافت نشد', 'status': 'nok', 'code': 401})
        data = json.loads(json_data)
        # {'username': email, 'password': password, 'cart-id': cartId, 'gender': gender, 'marketing': allowMarketing, 'personal': allowPersonalData}
        gender = data.get('gender', None)
        marketing = data.get('marketing', False)
        personal = data.get('personal', False)
        new_user = get_user_model().objects.filter(username=data['username'])
        if new_user.exists():
            return JsonResponse(data={'msg': f'کاربر {data["username"]} در حال حاضر وجود دارد', 'status': 'nok', 'code': 400})
        new_user = get_user_model().objects.create_user(username=data['username'], password=data['password'], gender=gender, marketing=marketing, personal=personal)
        if user_signup_login(request, new_user):
            # Synchronize Cart data with cart session data after login
            cart = new_user.cart_user.first()
            cart.sync_session_cart_after_authentication(request)
            # If user created successfully, direct him/her to his/her newly created profile
            return JsonResponse(data={'msg': f"کاربر جدید ساخته شد", 'status': 'ok', 'code': 201})
        # If there is a problem in 'user_signup_login' (eg: user could not login the website) redirect
        # the user to the main page
        return JsonResponse(data={'msg': 'کاربر جدید ایجاد شد اما لاگین انجام نشد', 'status': 'nok', 'code': 301})
    # If any method used except for 'POST', redirect user to 'login_signup' view
    else:
        return render(request, 'login/signup.html')


@login_required
def password_change(request):
    """Handles changing of user password"""
    if request.method == 'POST':
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'داده ای دریافت نشد', 'status': 'nok', 'code': 400})
        data = json.loads(json_data)
        password = data.get('password', None)
        password_new = data.get('password-new', None)
        if not password or not password:
            return JsonResponse(data={'msg': 'رمز عبور دریافت نشده', 'status': 'nok', 'code': 403})
        user = authenticate(request, username=request.user.username, password=password)
        if not user:
            return JsonResponse(data={'msg': 'رمز عبور اشتباه است', 'status': 'nok', 'code': 402})
        # If current password is valid, change user password with new-password
        user.password = make_password(password_new)
        user.save()
        # ? If we don't use "login(request, user)" after changing the password, user logout and see internal error
        # ! Provide for backen argument when google authentication implemented
        user = login(request, user)
        return JsonResponse(data={'msg': 'رمز عبور با موفقیت تغییر داده شد', 'status': 'ok', 'code': 200})
    # Any request method except for the 'POST" resulted in following error
    else:
        return JsonResponse(data={'msg': 'متد درخواستی اشتباه است', 'status': 'nok', 'code': 401})


@login_required
def edit_profile(request):
    """Edit user profile from dashboard"""
    if request.method == 'POST':
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'داده ای دریافت نشد', 'status': 'nok', 'code': 401})
        data = json.loads(json_data)
        first_name = data.get('first-name', None)
        last_name = data.get('last-name', None)
        phone = data.get('phone', None)
        address = data.get('address', None)
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.address = address
        user.save()
        return JsonResponse(data={'msg': 'اطلاعات شما با موفقیت تغییر کرد', 'status': 'ok', 'code': 200})
    # If any method requested except for POST returns following response
    return JsonResponse(data={'msg': 'متد اشتباهی ارسال شده', 'status': 'nok', 'code': 400})


@login_required
def edit_profile_image(request):
    """Edit user profile image in user dashboard"""
    if request.method == 'POST':
        files = request.FILES
        if not files:
            return JsonResponse(data={'msg': 'داده ای دریافت نشد', 'status': 'nok', 'code': 401})
        request.user.picture = files['image']
        request.user.save()
        return JsonResponse(data={'msg': 'تصویر با موفقیت تغییر پیدا کرد', 'status': 'ok', 'code': 200})
    else:
        return JsonResponse(data={'msg': 'متد اشتباهی ارسال شده', 'status': 'nok', 'code': 400})
