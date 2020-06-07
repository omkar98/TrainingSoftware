from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from main_portal.models import Update, UserDetail
from django.contrib.auth import authenticate, login
from django.db import IntegrityError
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth.decorators import user_passes_test
from django.conf import settings
from datetime import datetime, timedelta
from django.utils import timezone
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q


superusers = ['bisen_rg@mgmcen.ac.in','shivanip.vaidya@gmail.com', 'pratikshawalbe@gmail.com', 'sangamesh1439@gmail.com', 'jayeshukalkar@gmail.com', 'nikhilthakare14@gmail.com', 'edu.omkar@gmail.com']
# superusers=['edu.omkar@gmail.com']

def viewemailtemplate(request):
    return render(request, 'users/student_update_email.html')

@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def no_updates_email(request):
    student_updates = Update.objects.filter(date_posted__gte=datetime.now()-timedelta(days=1))
    list_of_students = []
    if not student_updates:
        users = User.objects.all()
        for user in users:
            list_of_students.append(user.email)
    else:
        for stud in student_updates:
            not_updated_student=User.objects.filter(~Q(email=stud.student.email))
        for stud in not_updated_student:
            list_of_students.append(stud.email)
    info={
        'submitted':student_updates,
        'users' : list_of_students,
        'title' : 'Not Updated Users'
    }
    subject = '[Update-Required] ReactJS 15-Days Training Course'
    html_message = render_to_string('users/student_update_email.html', {'info': info})
    plain_message =strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = list_of_students
    plain_text_1=f"Students who didnot yet submit their tasks are {list_of_students}"
    # send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)
    # send_mail(subject, f"List of students who didnot yet submit their updates : {list_of_students}", from_email, superusers, fail_silently=False)
    # messages.add_message(request, messages.SUCCESS,"message sent successfully.")
    print(info)
    return render(request, 'users/student_update_email.html',{'info':info})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def updates_email(request):
    all_user_details = []
    info={
        'title':'Email',
        'userDetails': all_user_details
    }
    if request.method == 'POST':
        form = request.POST.dict()
        how_many_days =  int(form['days'])
        updates = Update.objects.filter(date_posted__gte=datetime.now()-timedelta(days=how_many_days)).order_by('-date_posted')
        for update in updates:
            userDetails = UserDetail.objects.get(student=update.student)
            all_user_details.append([update, userDetails.student_class_cat[userDetails.student_class]])
        info={
            'title':'Email',
            'userDetails': all_user_details,
            'days':int(form['days'])
        }
        subject = '[Student-Updates] ReactJS Training Course'
        html_message = render_to_string('users/mail_template.html', {'info': info})
        plain_message =strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = superusers
        send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)
        messages.add_message(request, messages.SUCCESS,"message sent successfully.")
        print(info)
    return render(request, 'users/update_emails.html',{'info':info})

@login_required(login_url='/login')
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
        user_status = UserDetail.objects.get(student=user)
        if user is not None and user_status.status==1:
            login(request, user)
            print("login successful")
            messages.add_message(request, messages.SUCCESS,"Successfully logged in.")
            return redirect('user-dashboard')
        else:
            messages.add_message(request, messages.ERROR,"Please enter valid credentials.")
    return render(request, 'users/user-login.html', {'info':info})


def register(request):
    classes = UserDetail._meta.get_field('student_class').choices
    info = {
        'title': 'User-Registration',
        'classes':classes,
    }
    if request.method == 'POST':
        form = request.POST.dict()
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
            user_status = UserDetail(student=user, student_class=form['student_class'])
            user_status.save()
            messages.add_message(request, messages.SUCCESS,"Registered Successfully! Your registration will be approved by Admin within 24 Hrs.")
        return redirect('portal-home')
    else:
        return render(request, 'users/user-registration.html', {'info':info})
