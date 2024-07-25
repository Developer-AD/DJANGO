from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from django.conf import settings
from django.contrib import messages
import requests
from datetime import datetime

# -------------------------------------------- Loging Page ------------------------------------
def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            check_user = MyUser.objects.filter(username=username)

            if not check_user.exists():
                messages.error(
                    request, "Username not found, Kindly try again...!")
                return redirect('login')

            user = authenticate(username=username, password=password)

            print('-------------- Login Details Start -----------------')
            print(username)
            print(password)
            print(user)
            print('-------------- Login Details End -----------------')

            if user is not None:
                # Recapcha authentication.
                # site_key = request.POST['g-recaptcha-response']
                # capchaData = {
                #     'secret': settings.SECRET_KEY,
                #     'response': site_key
                # }

                # post_url = 'https://www.google.com/recaptcha/api/siteverify'
                # res = requests.post(post_url, data=capchaData)
                # verify = res.json()['success']

                # For test purposes Google recapcha will return True.
                verify = True

                if verify:
                    if user.role == 1:    
                        login(request, user)
                        return redirect(request.GET.get('next', "admin_dashboard"))

                    elif user.role == 2:    
                        login(request, user)
                        return redirect(request.GET.get('next', "user_dashboard"))

                    else:
                        messages.error(request, "Invalid Role")
                        return redirect('login')

                messages.error(request, 'Invalid Captcha Please Try Again')
                return redirect('login')

            messages.error(request, "Wrong Credentials")
            return redirect('login')

        except Exception as e:
            print(e)
            messages.error(request, "Something went wrong")
            return redirect('login')

    return render(request, 'login.html', {'site_key': settings.SITE_KEY})


# -------------------------------------------- Logout Page ------------------------------------
def logout_page(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully...!')
    return redirect('login')

# --------------------------------------------- Roles --------------------------------------
def AdminRole(user):
    return user.role == 1

def UserRole(user):
    return user.role == 2

# --------------------------------------------- Dashboard --------------------------------------

def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            conf_password = request.POST.get('conf_password')
            # email = request.POST.get('email')
            # phone = request.POST.get('phone')
            print('-------------- Registration Details Start -----------------')
            print(username)
            print(email)
            print(password)
            print(conf_password)
            print('-------------- Registration Details End -----------------')

            user = MyUser.objects.filter(username=username)
            if user.exists():
                messages.error(
                    request, "Username already exists, Kindly choose a different one...!")
                return redirect('register')

            if password != conf_password:
                messages.error(
                    request, "Passwords do not match, Kindly try again...!")
                return redirect('register')

            MyUser.objects.create_user(username=username, password=password)
            messages.success(
                request, "User account has been created successfully...!")
            return redirect('login')

        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('register')

    return render(request, 'register.html')

# --------------------------------------------- Admin Dashboard --------------------------------------
# @login_required(login_url="/")
def dashboard(request):
    students = Student.objects.all()
    contexts = {'students': students}
    # messages.success(request, "Welcome to Student Dashboard")
    return render(request, 'dashboard.html', contexts)


@login_required(login_url="/login")
@user_passes_test(AdminRole, login_url="/login")
def admin_dashboard(request):
    students = Student.objects.all()
    contexts = {'students': students}
    # messages.success(request, "Welcome to Student Dashboard")
    return render(request, 'admin_dashboard.html', contexts)


# --------------------------------------------- User Dashboard --------------------------------------
@login_required(login_url="/login")
@user_passes_test(UserRole, login_url="/login")
def user_dashboard(request):
    students = Student.objects.all()
    contexts = {'students': students}
    # messages.success(request, "Welcome to Student Dashboard")
    return render(request, 'user_dashboard.html', contexts)


# ------------ Upload Data Starts ------------------
@login_required(login_url="/login")
def student_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        photo = request.FILES.get('photo')

        print('-------------- Student Details Start -----------------')
        print(name)
        print(email)
        print(age)
        print(phone)
        print(photo)
        print('-------------- Student Details End -----------------')

        Student.objects.create(name=name, email=email,
                               age=age, phone=phone, photo=photo)
        messages.success(
            request, "Student record has been created successfully")

        return redirect('user_dashboard')
    return render(request, 'student_add.html')

# ------------ Upload Data Starts ------------------
@login_required(login_url="/")
def student_edit(request, id):
    student = Student.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        age = request.POST.get('age')
        phone = request.POST.get('phone')
        photo = request.FILES.get('photo')

        print('-------------- Student Update Details Start ----------------')
        print(name)
        print(email)
        print(age)
        print(phone)
        print(photo)
        print('-------------- Student Update Details End -----------------')

        student.name = name
        student.email = email
        student.age = age
        student.phone = phone
        student.photo = photo
        student.save()
        messages.success(
            request, "Student record has been updated successfully")

        return redirect('dashboard')
    return render(request, 'student_edit.html', {'student': student})


@login_required(login_url="/")
def student_delete(request, id):
    student = Student.objects.get(id=id)
    student.delete()
    messages.success(request, "Student record has been deleted successfully")
    return redirect('dashboard')

def send_email_attachment(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            
            pdf = DemoFiles.objects.first().pdf
            image = DemoFiles.objects.first().image

            # file_path = pdf.path
            file_path = image.path
            
            print('------------------------------ Email Start ----------------------------------')
            print(email)
            print(pdf)
            print(image)
            print(file_path)
            print('------------------------------ Email Ends ----------------------------------')

            message = 'Test email template to send attachments.'
            subject = 'Send Attachment'
            file_name = 'Attachment'

            # ---------------------- Send Normal Email Message --------------------------------
            # res = send_mail(subject, message,
            #                 settings.EMAIL_HOST_USER, [email])
            # return HttpResponse(f'Email Sent : {res}')


            # ---------------------- Send Attachment along with Email Message --------------------------------
            try:
                mail = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [email])
                with open(file_path, 'rb') as f:
                    # mail.attach(file_name, f.read(), 'application/pdf')
                    mail.attach(file_name, image.read(), 'image/jpeg')
                    mail.send()
                    messages.success(request, "Email sent successfully")
                    return HttpResponse("Email sent successfully")

            except Exception as e:
                messages.error(request, f"Failed to send email: {e}")
                return HttpResponse(f"{e}")


        except Exception as e:
            messages.error(request, "Something went wrong")
            return HttpResponse(f"{e}")
    return render(request, 'send_email.html')
