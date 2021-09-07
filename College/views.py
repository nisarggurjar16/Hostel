from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Students.models import *


def AboutUs(request):
    return render(request, 'about.html')


def Contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(name, email, subject, message)
        ContactForm.objects.create(
            name=name, email=email, subject=subject, message=message)
        return redirect('home')
    return render(request, 'contact.html')


def LoginSignupForm(request):
    if request.user.is_authenticated:
        return redirect('home')
    errorPWD = False
    errorLogin = False
    errorUsername = False
    if 'signup' in request.POST:
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        pwd1 = request.POST.get('pwd1')
        pwd2 = request.POST.get('pwd2')
        user = request.POST.get('user')
        mob = request.POST.get('mob')
        fees = request.POST.get('fees')
        pic = request.FILES.get('profile')
        percent = request.POST.get('percent')
        if pwd1 == pwd2:

            existingUser = User.objects.filter(username=user).first()
            if existingUser:
                errorUsername = True
            else:
                user = User.objects.create_user(
                    first_name=fname, last_name=lname, email=email, password=pwd1, username=user)
                student = StudentInformation.objects.create(
                    user=user, mobile=mob, profilePicture=pic, monthlyFees=fees, percentage=percent)
                if int(student.percentage) > 60:
                    user.is_staff = True
                    user.save()
                check = authenticate(username=user, password=pwd1)
                if check:
                    login(request, check)
                    return redirect('home')
                else:
                    errorLogin = True
        else:
            errorPWD = True

    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        check = authenticate(username=username, password=password)
        if check:
            login(request, check)
            return redirect('home')
        else:
            errorLogin = True
    d = {'errorLogin': errorLogin, "errorPWD": errorPWD,
         "errorUsername": errorUsername}
    return render(request, 'login.html', d)


def Logout(request):
    logout(request)
    return redirect('home')
