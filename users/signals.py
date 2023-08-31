from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.dispatch import receiver
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
# ! Using allauth signals to syncronize session and user cart
from allauth.account.signals import user_signed_up, user_logged_in

import decimal
import re


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def count_user_score_and_profile_discount(sender, instance, **kwargs):
    """Count user account score"""
    def score_count_helper(instance_score, discount_multiplier):
        """Helper function for DRY"""
        # It is highly recommended to set default and arbitrary values in 'django-constance' rather
        # than hardcoded in codes like this.
        instance.discount_value += decimal.Decimal(10000 * discount_multiplier)
        instance.score_lifetime += instance_score
        instance.score = 0

    score = instance.score
    if 500 <= score <= 1000:
        score_count_helper(score, 1)
    elif 1000 < score <= 1500:
        score_count_helper(score, 2)
    elif instance.score > 1500:
        score_count_helper(score, 3)


@receiver(pre_save, sender=settings.AUTH_USER_MODEL)
def fill_slug_field(sender, instance, **kwargs):
    """Fill slug field for user"""
    if not instance.slug:
        instance.slug = slugify(instance.username)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def fill_phone_email_on_username(sender, instance=None, created=False, **kwargs):
    """If username is based on phone or email, fill another field accordingly"""
    if created:
        regex_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        regex_phone =  re.compile(r'09[0-3][0-9]-?[0-9]{3}-?[0-9]{4}')
        if re.fullmatch(regex_email, instance.username):
            instance.email = instance.username
            instance.save()
        elif re.fullmatch(regex_phone, instance.username):
            instance.phone = instance.username
            instance.save()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def set_if_social_login_field(sender, instance=None, created=False, **kwargs):
    """To set if a user login with social_login, check if the user 'password' is empty"""
    if created and not instance.password:
        instance.is_social_login = True
        instance.user_db_backend = 'social'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_cart_after_user_created(sender, instance, created, *args, **kwargs):
    """Create a cart for user after user created"""
    if created:
        instance.cart_user.create()




# ! Django allauth signals recalled here

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    """Overwrite allauth user_signed_up signal. Everytime user signup with social login this signal recalled"""


@receiver(user_logged_in)
def user_logged_in(request, user, **kwargs):
    """Overwrite allauth user_logged_in signal. Everytime a user signin or even signup, this signal called. This is where we synchronize user session and its cart"""
    cart = user.cart_user.first()
    cart.sync_session_cart_after_authentication(request)
