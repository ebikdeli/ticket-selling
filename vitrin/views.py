from django.shortcuts import render, HttpResponse
from ticket.models import Ticket


def index(request):
    """Index page of the shop"""
    return HttpResponse('<div style="text-align: center;"><h1>Welcome to trenydol</h1></div>')
    # return render(request, 'vitrin/index.html')


def show_tickets(request):
    """Show all active tickets to the user"""
    return render(request, '')
