"""
Every user connect to the website for the first time, has a cart session created for them.
Important: Before any view called, A Cart and cart sessions must be created for any user either authenticated or Not.
"""
from . import cart_functions
from .models import Cart


class InitialSessionMiddleware:
    """Find the needed sessions for the user and if couldn't find them, create them"""
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Code to be executed for each request before the view (and later
        middleware) are called.
        """
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Called just before Django calls the view.
        """
        # ? If session_key has not been created already, create it
        if not request.session.exists(request.session.session_key):
            request.session.create()
        # If cart sessions are not created already, create them
        try:
            cart_functions.get_cart_session(request)
        except KeyError:
            cart_functions.reset_session(request)
        # Get or create Cart for unauthenticated users with the session_key
        if not request.user.is_authenticated:
            cart = cart_functions.get_or_create_cart_unauth_session_key(Cart, request)
        # Get or create Cart object for the athenticated user
        else:
            cart = cart_functions.get_or_create_cart_auth_session_key(Cart, request)
        # If cart is None it means there is a bug in our code
        if cart:
            request.session['cart_id'] = cart.id
        else:
            request.session['cart_id'] = 0
            # ! If there is no Cart get or created before, create a new Cart for current user
            new_cart = Cart.objects.create()
            if request.user.is_authenticated:
                new_cart.user = request.user
                new_cart.save()
            request.session['cart_id'] = int(new_cart.id)
        # MiddleWare process_view method should return None
        return None
