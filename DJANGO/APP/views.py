from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

            user = User.objects.filter(username=username)

            if not user.exists():
                messages.error(request, "Username not found, Kindly try again...!")
                return redirect('login')

            user = authenticate(username=username, password=password)

            if user is not None:
                # Recapcha authentication.
                site_key = request.POST['g-recaptcha-response']
                capchaData = {
                    'secret': settings.SECRET_KEY,
                    'response': site_key
                }

                post_url = 'https://www.google.com/recaptcha/api/siteverify'
                res = requests.post(post_url, data=capchaData)
                verify = res.json()['success']

                if verify:
                    login(request, user)
                    return redirect(request.GET.get('next', "dashboard"))

                messages.error(request, 'Invalid Captcha Please Try Again')
                return redirect('login')
            

            messages.error(request, "Wrong Credentials")
            return redirect('login')

        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('login')

    return render(request, 'login.html', {'site_key': settings.SITE_KEY})


# -------------------------------------------- Logout Page ------------------------------------
def logout_page(request):
    logout(request)
    return redirect('login')

# --------------------------------------------- Dashboard --------------------------------------
def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            conf_password = request.POST.get('conf_password')
            # email = request.POST.get('email')
            # phone = request.POST.get('phone')

            user = MyUser.objects.filter(username=username)
            if user.exists():
                messages.error(request, "Username already exists, Kindly choose a different one...!")
                return redirect('register')
            
            if password != conf_password:
                messages.error(request, "Passwords do not match, Kindly try again...!")
                return redirect('register')

            MyUser.objects.create_user(username=username, password=password)
            messages.success(request, "User account has been created successfully...!")
            return redirect('login')

        except Exception as e:
            messages.error(request, "Something went wrong")
            return redirect('register')
            
    return render(request, 'register.html')

# --------------------------------------------- Dashboard --------------------------------------
@login_required(login_url="/")
def dashboard(request):
    contexts = {}
    return render(request, 'dashboard.html', contexts)


# ------------ Upload Data Starts ------------------
@login_required(login_url="/")
def create(request):
    if request.method == 'POST':
        db_name = request.POST.get('db_name')
        db_file = request.FILES.get('db_file')

        current_date = datetime.now().date()

        Model.objects.create()

        return redirect('create')
    return render(request, 'create.html', contexts)


@login_required(login_url="/")
def delete_contact(request, id):
    db = Database.objects.get(id=id)
    db.delete()
    return redirect('create_contact')


@login_required(login_url="/")
def edit_contact(request, id):
    db = Database.objects.get(id=id)
    if request.method == 'POST':
        db_name = request.POST.get('db_name')
        db_file = request.FILES.get('db_file')

        if db_file:
            strn_data, data_records = get_excel_data(db_file)
            db.db_data = strn_data
            db.db_records = data_records

        current_date = datetime.now().date()
        db.db_name = db_name
        db.creation_date = current_date
        db.save()
        return redirect('create_contact')

    return HttpResponse('Edit Data')