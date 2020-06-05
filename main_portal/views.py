from django.shortcuts import render
from .models import Update
from django.contrib import messages
def home(request):
    info = {
        'title': 'Home',
    }
    return render(request, 'main_portal/home.html', {'info':info})

def participants(request):
    info = {
        'title': 'Participants',
    }
    return render(request, 'main_portal/construction.html', {'info':info})

def announcements(request):
    info = {
        'title': 'Announcements',
    }
    return render(request, 'main_portal/construction.html', {'info':info})

def schedule(request):
    info = {
        'title': 'Schedule',
    }
    return render(request, 'main_portal/construction.html', {'info':info})


def downloads(request):
    info = {
        'title': 'Downloads',
    }
    return render(request, 'main_portal/construction.html', {'info':info})

def gallery(request):
    info = {
        'title': 'Gallery',
    }
    return render(request, 'main_portal/construction.html', {'info':info})

def contacts(request):
    info = {
        'title': 'Contacts',
    }
    return render(request, 'main_portal/construction.html', {'info':info})
