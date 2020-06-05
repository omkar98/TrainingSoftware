from django.shortcuts import render
from .models import Update
from django.contrib import messages
def home(request):
    info = {
        'title': 'Home',
    }
    return render(request, 'main_portal/home.html', {'info':info})
