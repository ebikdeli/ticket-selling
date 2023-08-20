from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """View user dashboard and can change their profile data and password here"""
    return render(request, 'dashboard/profile.html')
