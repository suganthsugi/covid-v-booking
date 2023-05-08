from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as reallogin
from django.core.mail import send_mail
from django.conf import settings
from .models import *
import random
# Create your views here.

def register(request):
    usernames = [user.username for user in User.objects.all()]
    emails = [user.email for user in User.objects.all()]
    context={'alluser':usernames, 'allemail':emails}
    if(request.method=='POST'):
        uname = request.POST['uname']
        email = request.POST['email']
        emailotp = request.POST['emailotp']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['password']
        if(EmailVerification.objects.filter(email=email).exists()):
            requireOtp = EmailVerification.objects.get(email=email).otp
            print(requireOtp, emailotp)
            if(str(requireOtp)==str(emailotp)):
                user = User.objects.create_user(username=uname, email=email, password=pass1)
                user.first_name = fname
                user.last_name = lname
                user.save()
                messages.success(request, 'Your message here')
                request.session['context_data'] = {'msg': 'Account created successfully. Please Login to continue...', 'color':'success'}
                # tcontext={'msg':'Account created successfully. Please Login to continue...', 'color':'success'}
                return redirect('login')
            else:
                tverifyEmailURL=reverse('verifyEmail')
                tcontext={'msg':f'''Please enter correct OTP, which has been sent to email. Or validate email once again. <a href="{tverifyEmailURL}">Verify Mail</a>''', 'color':'danger'}
                return render(request, 'register.html', tcontext)
        else:
            tverifyEmailURL=reverse('verifyEmail')
            tcontext={'msg':f'''Your email is not yet verified, please verify your email to continue. <a href="{tverifyEmailURL}">Verify Mail</a>''', 'color':'warning'}
            return render(request, 'register.html', tcontext)
    return render(request, 'register.html', context)

def login(request):
    if(request.method=='POST'):
        cemail = request.POST['email']
        pass1 = request.POST['pass1']
        uname=""
        if(User.objects.filter(email=cemail).exists()):
            uname=User.objects.filter(email=cemail).first().username
        currentUser = authenticate(username=uname, password=pass1)
        if(currentUser is not None):
            reallogin(request, currentUser)
            url = reverse('listcentre')
            return redirect(url)
        else:
            if(currentUser is None):
                msg={'err':f'The Username or Password is incorrect. Please try again'}
                return render(request, 'login.html', msg)
    context = {'data': request.session.get('context_data')}
    return render(request, 'login.html', context)

def verifyEmail(request):
    if(request.method == 'POST'):
        email = request.POST['email']
        otp=random.randint(100000, 999999)
        send_mail(
            "Covidvaccine Booking Email Verfication OTP",
            f"Your email activation password is {otp}",
            'covidvaccinebooking1@gmail.com',
            [email],
            fail_silently=False
        )
        # print(f'mail sent {otp}')
        tcontext={'msg':'Check your email for Email Verification OTP. Note: check the spam folder'}
        if(EmailVerification.objects.filter(email=email).exists()):
            curr = EmailVerification.objects.get(email=email)
            curr.otp = otp
            curr.save()
        else:
            newemail = EmailVerification(email=email, otp=otp)
            newemail.save()
        return render(request, 'register.html', tcontext)
    context={}
    return render(request, 'email_verification.html', context)


def logout(request):
    auth.logout(request)
    
    return redirect(login)

def forgotPassword(request):
    context={}
    return render(request, 'forgot_password.html', context)

def adminLogin(request):
    if request.method == 'POST':
        username = request.POST['fname']
        password = request.POST['pass1']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print("yes")
            reallogin(request, user)
            url = reverse('listcentre')
            return redirect(url)
        else:
            context = {'error_message': 'Invalid credentials'}
            return render(request, 'adminlogin.html', context)
    else:
        return render(request, 'adminlogin.html')