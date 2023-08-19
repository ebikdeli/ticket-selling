from django.shortcuts import render
from django.http import JsonResponse
from .models import Faq, UserMessage, Rule
import json
from constance import config



def about_contact_us(request):
    """Both pages of about us and contact us are integrated into one page"""
    context = {'config': config}
    return render(request, 'support/about-contact-us.html', context)


def rule(request):
    """Rules page that consist of rules to using and interacting with the website"""
    rule = Rule.objects.first() if Rule.objects.all().exists() else None
    context = {'rule': rule}
    return render(request, 'support/rules.html', context)


def faq(request):
    """Frequently asked question page. This page includes a form to customers and users send message to the site"""
    faqs = Faq.objects.all()
    context = {'faqs': faqs}
    return render(request, 'support/faq.html', context)


def user_message_form(request):
    """Every messages user send processed here"""
    if request.method == 'POST':
        # * Process received data and check if there is no error
        json_data = request.POST.get('data', None)
        if not json_data:
            return JsonResponse(data={'msg': 'دیتایی دریافت نشد', 'code': 402, 'status': 'nok'})
        data = json.loads(json_data)
        email = data.get('email', None)
        message = data.get('message', None)
        if not email:
            return JsonResponse(data={'msg': 'ایمیل دریافت نشد', 'code': 409, 'status': 'nok'})
        if not message:
            return JsonResponse(data={'msg': 'پیامی دریافت نشد', 'code': 410, 'status': 'nok'})
        UserMessage.objects.create(email=email, message=message)
        return JsonResponse(data={'msg': 'پیام با موفقیت ارسال شد', 'code': 200, 'status': 'ok'})
