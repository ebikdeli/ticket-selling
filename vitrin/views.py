from django.shortcuts import render, HttpResponse
from ticket.models import Ticket
from cart.models import Cart


def index(request):
    """Index page of the shop"""
    tickets = Ticket.objects.order_by('-updated')[:20]
    if request.user.is_authenticated:
        cart = request.user.cart_user.first()
    else:
        cart_qs = Cart.objects.filter(session_key=request.session.session_key)
        if cart_qs.exists():
            cart = cart_qs.get()
        else:
            request.session.create()
            cart = Cart.objects.create(session_key=request.session.session_key)
    ticketsolds = cart.ticketsold_cart.all()
    context = {'tickets': tickets, 'ticketsolds': ticketsolds}
    return render(request, 'vitrin/index.html', context)
