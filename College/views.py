from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from Students.models import *
from django.conf import settings
from django.template.loader import get_template
import requests
from django.core.mail import EmailMultiAlternatives
import json

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
                sub = "Student Account Created Successfully"
                data = {"name":fname, "username":user}
                html = get_template("mail.html").render(data)
                from_mail = settings.EMAIL_HOST_USER
                msg = EmailMultiAlternatives(sub, '', from_mail, [email])
                msg.attach_alternative(html, 'text/html')
                msg.send()
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
            if request.user.is_superuser:
                return redirect('admin')
            return redirect('home')
        else:
            errorLogin = True
    d = {'errorLogin': errorLogin, "errorPWD": errorPWD,
         "errorUsername": errorUsername}
    return render(request, 'login.html', d)


def Logout(request):
    logout(request)
    return redirect('home')


def AdminPanel(request):
    if not request.user.is_superuser:
        return redirect('home')
    
    students = StudentInformation.objects.all()
    return render(request, 'admin.html', {"students":students})


def DeleteStudent(request, uid):
    usr = User.objects.filter(id = uid)
    usr.delete()
    return redirect('admin')

headers = { "X-Api-Key": "d82016f839e13cd0a79afc0ef5b288b3", "X-Auth-Token": "3827881f669c11e8dad8a023fd1108c2"}


def PaymentDecline(request):
    return render(request, 'payerror.html')

def Payment(request, sid):
    student = StudentInformation.objects.get(id = sid)
    mob = student.mobile
    purp = "Hostel Fees"
    amt = student.monthlyFees
    email = student.user.email
    name = student.user.username

    payload = {
        "purpose":purp,
        "amount":amt,
        "buyer_name":name,
        "email":email,
        "phone":mob,
        "send_mail":True,
        "send_sms":True,
        "redirect_url":""
    }

    response = requests.post("https://www.instamojo.com/api/1.1/payment-requests/", data=payload, headers=headers)
    print(response)
    y = response.text
    d = json.loads(y)
    a = d["payment_request"]["longurl"]
    i = d["payment_request"]["id"]
    PaymentDetail.objects.create(std = student, pay_id = i)
    return redirect(a)


def payment_check(request, sid):
    pay = False
    i = PaymentDetail.objects.filter(id = sid).last()
    ii = i.pay_id
    response = requests.get("https://www.instamojo.com/api/1.1/payment-requests/" + ii + '/', headers=headers)
    y = response.text
    d = json.loads(y)
    status = ["payment_request"]["status"]
    if status == "Complete":
        i.status = status
        return redirect("admin")
    else:
        return redirect("payfail")
    