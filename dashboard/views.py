from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile(request):
    """View user dashboard and can change their profile data and password here"""
    print(request.session.items())
    print(request.session.session_key)
    return render(request, 'dashboard/profile.html')
