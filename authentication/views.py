from http.client import HTTPResponse
from re import M
from telnetlib import LOGOUT
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from storefront import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from . tokens import generate_token
from django.core.mail import EmailMessage, send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# Create your views here.

def home(request):
    return render(request,"authentication/index.html")

def signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"Email already registered!")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request, "Username must be under 10 characters!")

        if pass1 != pass2:
            messages.error(request, "Password mismatch!")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!")
            return redirect('home')

        my_user = User.objects.create_user(username, email, pass1)
        my_user.first_name = fname
        my_user.last_name = lname
        # my_user.is_active = False

        my_user.save()

        messages.success(request, "Registered Successfully! We have sent you a confirmation email, please confirm your email in order to activate your account.")

        # Welcome Email

        # subject = "Welcome to Our Page!"
        # message = "Hello " + my_user.first_name + "!! \n" + "Welcome to HCL!! \n Thank you for visiting this page \n We have also sent you a confirmation email, please confirm your email address in order to activate your account. \n\n Thank You\n Kushagra Saxena"
        # from_email = settings.EMAIL_HOST_USER
        # to_list = [my_user.email]
        # send_mail(subject, message, from_email, to_list, fail_silently=True)

        #Email Address Confirmation Email

        # current_site = get_current_site(request)
        # email_subject = "Confirm your email address!"
        # message2 = render_to_string('email_confirmation.html',{
        #     'name' : my_user.first_name,
        #     'domain' : current_site.domain,
        #     'uid' : urlsafe_base64_encode(force_bytes(my_user.pk)),
        #     'token' : generate_token.make_token(my_user)
        # })
        # email = EmailMessage(
        #     email_subject,
        #     message2,
        #     settings.EMAIL_HOST_USER,
        #     [my_user.email],
        # )
        # email.fail_silently = True
        # email.send()

        return redirect('signin')

    return render(request,"authentication/signup.html")

def signin(request):

    if request.method == "POST":
        
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request,user)
            fname = user.first_name
            return render(request, "authentication/index.html", {"fname":fname})

        else:
            messages.error(request, "Bad Credentials!")
            return redirect('home')

    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"Logged out successfully!")
    return redirect('home')

# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         my_user = User.objects.get(pk=uid)

#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         my_user = None

#     if my_user is not None and generate_token.check_token(my_user,token):
#         my_user.is_active = True
#         my_user.save()
#         login(request, my_user)
#         return redirect('home')

#     else:
#         return render(request, 'activation_failed.html')