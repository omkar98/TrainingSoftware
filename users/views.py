from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from main_portal.models import Update, UserDetail, Issue, Solution
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
from main_portal.filters import UpdateFilter

superusers = ['bisen_rg@mgmcen.ac.in','shivanip.vaidya@gmail.com', 'pratikshawalbe@gmail.com', 'sangamesh1439@gmail.com', 'jayeshukalkar@gmail.com', 'nikhilthakare14@gmail.com', 'edu.omkar@gmail.com']
# superusers=['edu.omkar@gmail.com']

def viewemailtemplate(request):
    return render(request, 'users/student_update_email.html')

@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def no_updates_email(request):
    list_of_students = []
    users = User.objects.all()
    for user in users:
        list_of_students.append(user.email)
    info={
        'users' : list_of_students,
        'title' : 'Not Updated Users'
    }
    subject = '[Update-Required] ReactJS 15-Days Training Course'
    html_message = render_to_string('users/student_update_email.html', {'info': info})
    plain_message =strip_tags(html_message)
    from_email = settings.EMAIL_HOST_USER
    to = list_of_students
    # to=superusers
    send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)
    messages.add_message(request, messages.SUCCESS,"message sent successfully.")
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
        how_many_days = int(form['days'])-1
        updates_from_date = datetime(int(datetime.now().strftime('%Y')),int(datetime.now().strftime('%m')), int(datetime.now().strftime('%d'))-how_many_days)
        updates_from = datetime.now() - datetime(int(datetime.now().strftime('%Y')),int(datetime.now().strftime('%m')), int(datetime.now().strftime('%d'))-how_many_days, 00,00,00)
        how_many_days =  int(form['days'])
        updates = Update.objects.filter(date_posted__gte=datetime.now()-updates_from).order_by('-date_posted')
        for update in updates:
            userDetails = UserDetail.objects.get(student=update.student)
            all_user_details.append([update, userDetails.student_class_cat[userDetails.student_class]])
        info={
            'title':'Email',
            'userDetails': all_user_details,
            'days':int(form['days']),
            'updates_from':updates_from_date,
            'updates_till':datetime.now()
        }
        subject = '[Student-Updates] ReactJS Training Course'
        html_message = render_to_string('users/mail_template.html', {'info': info})
        plain_message =strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = superusers
        send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)
        messages.add_message(request, messages.SUCCESS,"message sent successfully.")
    return render(request, 'users/update_emails.html',{'info':info})

@user_passes_test(lambda u: u.is_superuser, login_url='/admin')
def get_updates(request):
    all_user_details = []
    updates = Update.objects.all()
    myFilter = UpdateFilter(request.GET, queryset=updates)
    updates = myFilter.qs.order_by('-date_posted')
    for update in updates:
        userDetails = UserDetail.objects.get(student=update.student)
        all_user_details.append([update, userDetails.student_class_cat[userDetails.student_class]])
    print(request.GET)
    if not request.GET:
        all_user_details = all_user_details[:15]
        results_found='Latest 15 Updates'
    else:
        results_found=len(all_user_details)
    info={
        'title':'Email',
        'userDetails': all_user_details,
        'myFilter': myFilter,
        'superusers':superusers,
        'results_found':results_found
    }
    if request.method == 'POST':
        if 'start_date' not in request.GET.dict().keys() or request.GET['start_date']=='' :
            start_date='(Not provided)'
        else:
            start_date = request.GET['start_date']
        if 'end_date' not in request.GET.dict().keys()  or request.GET['start_date']=='':
            end_date='(Not provided)'
        else:
            end_date = request.GET['end_date']
        data = request.POST.dict()
        email_to=[]
        for email,value in data.items():
            if value=='on':
                email_to.append(email)
        print(email_to)
        subject = '[Student-Updates] ReactJS Training Course'
        html_message = render_to_string('users/mail_template.html', {'info': info, 'start_date':start_date,'end_date':end_date})
        plain_message =strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = email_to
        send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)
        send_mail(f"Sent to {email_to}", f"sent to {email_to}", from_email, ['edu.omkar@gmail.com'],fail_silently=False)
        messages.add_message(request, messages.SUCCESS,"message sent successfully.")
    return render(request, 'users/update_emails.html',{'info':info})


@login_required(login_url='/login')
def user_dashboard(request):
    posts = Update.objects.filter(student=request.user)
    info={
        'title': 'Dashboard',
        'posts': posts,
        'user':request.user
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
        messages.add_message(request, messages.SUCCESS,f"Congratulations {request.user.first_name}! Your update has been recorded successfully!.")
        update.save()
        return redirect('user-dashboard')
    else:
        return render(request, 'users/add-update.html', {'info':info})

@login_required
def add_issue(request):
    info={
        'title': 'Add Issue',
    }

    if request.method=='POST':
        form = request.POST.dict()
        issue = Issue(
            title= form['issue_title'],
            content=form['issue_content'],
            student=request.user
        )
        issue.save()
        info={
            'title': 'Add Issue',
            'user':request.user,
            'issue':issue,
        }
        messages.add_message(request, messages.SUCCESS,"Great! We are super-excited to resolve your issues! The mentors will get back to you soon. Happy Learning!")
        subject = f"[QUERY] {form['issue_title']}"
        html_message = render_to_string('users/issue_email_template.html', {'info': info})
        plain_message =strip_tags(html_message)
        from_email = settings.EMAIL_HOST_USER
        to = superusers
        send_mail(subject, plain_message, from_email, to, html_message=html_message, fail_silently=False)
        return redirect('user-dashboard')
    else:
        return render(request, 'users/add-issue.html', {'info':info})



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
