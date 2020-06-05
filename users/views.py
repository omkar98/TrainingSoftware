from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from main_portal.models import Update, UserApproval
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required
def user_dashboard(request):
    posts = Update.objects.filter(student=request.user)
    info={
        'title': 'Dashboard',
        'posts': posts,
    }
    return render(request, 'users/user-dashboard.html', {'info':info})

@login_required
def add_update(request):
    info={
        'title': 'Add Update',
    }

    if request.method=='POST':
        form = request.POST.dict()
        update = Update(
            title= form['update_title'],
            content=form['update_content'],
            student=request.user
        )
        print(update)
        messages.add_message(request, messages.SUCCESS,"Updated Successfully.")
        update.save()
        return redirect('user-dashboard')
    else:
        return render(request, 'users/add-update.html', {'info':info})


def logout_view(request):
    logout(request)
    return redirect('portal-home')

def user_login(request):
    info={
        'title': 'Login-Page',
    }
    if request.method=='POST':
        form = request.POST.dict()
        username=form['student_email']
        password=form['student_password']
        user = authenticate(request, username=username, password=password)
        user_status = UserApproval.objects.get(student=user)
        if user is not None and user_status.status==1:
            login(request, user)
            print("login successful")
            messages.add_message(request, messages.SUCCESS,"Successfully logged in.")
            return redirect('user-dashboard')
        else:
            messages.add_message(request, messages.ERROR,"Please enter valid credentials.")
    return render(request, 'users/user-login.html', {'info':info})


def register(request):
    info = {
        'title': 'User-Registration',
    }
    if request.method == 'POST':
        form = request.POST.dict()
        # print()
        try:
            user = User.objects.create_user(
                    username = form['student_email'],
                    password = form['student_password'],
                    email = form['student_email'],
                    first_name = form['student_first_name'],
                    last_name = form['student_last_name']
                )
        except IntegrityError:
            messages.add_message(request, messages.ERROR,"Already Registered User. Please try login.")
            return render(request, 'users/user-registration.html', {'info':info})
        else:
            user.save()
            user_status = UserApproval(student=user)
            user_status.save()
            messages.add_message(request, messages.SUCCESS,"Registered Successfully! Your registration will be approved by Admin within 24 Hrs.")
        return redirect('portal-home')
    else:
        return render(request, 'users/user-registration.html', {'info':info})
