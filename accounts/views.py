from django.shortcuts import render,redirect
from accounts.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from accounts.models import EmailOTP
from django.contrib.auth import login,logout,update_session_auth_hash
from .utils import custom_authenticate
from django.contrib.auth.decorators import login_required

from django.urls import reverse
# Create your views here.

import random



def register(request):
    EUFO=UserProfileForm()
    d={'EUFO':EUFO}

    if request.method=='POST':
        UFO=UserProfileForm(request.POST)
        if UFO.is_valid():
            user = UFO.save(commit=False)
            password = UFO.cleaned_data['password']
            user.set_password(password)    
            user.is_active = True           
            user.save() 
            memail=UFO.cleaned_data['email']
            #genrate otp
            
            otp=random.randint(100001,999998)
            EOTFO=EmailOTP.objects.create(email=memail, otp_code=otp)
            #send otp
            send_mail(
                'OTP for Registration',
                f'Your OTP is {otp} \n  This OTP is valid for 10 minutes',
                'lokeshpatel2714@gmail.com',
                [memail],
                fail_silently=True,
            )
            return HttpResponseRedirect('/otp_verification')
        
    return render(request,'register.html',d)
    

def otp_verification(request):
    EOTPF=EmailOTPForm()
    d={'EOTPF':EOTPF}
    if request.method=='POST':
        OTPVF=EmailOTPForm(request.POST)
        if OTPVF.is_valid():
            email=OTPVF.cleaned_data['email']
            otp_code=OTPVF.cleaned_data['otp_code']
            try:
                EOTP=EmailOTP.objects.get(email=email,otp_code=otp_code)
                if EOTP.is_expired():
                    messages.error(request, 'OTP expired. Please register again.')
                    return HttpResponseRedirect('/register')
                else:
                    user=UserProfile.objects.get(email=email)
                    user.is_active=True
                    user.save()
                    EOTP.delete()
                    send_mail(
                        'Registration Sucessful',
                        'Your registration is successful',
                        'lokeshpatel2714@gmail.com',
                        [email],
                        fail_silently=True,
                    )
                    return HttpResponse('Registration successful')
                
            except EmailOTP.DoesNotExist:
                messages.error(request,'Invalid OTP')
                return HttpResponseRedirect('/otp_verification')

    return render(request,'otp_verification.html',d)



def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        UO = custom_authenticate(email=email, password=password)  
        if UO is not None:
            login(request, UO)  
            return HttpResponseRedirect(reverse('home'))  
        else:
            return HttpResponseRedirect(reverse('user_login'))
    return render(request, 'user_login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('oldpassword')
        new_password = request.POST.get('password')
        user = request.user
        if user.check_password(old_password):
            user.set_password(new_password)  
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "✅ Password changed successfully.")
            return redirect('home')
        else:
            messages.error(request, "❌ Old password is incorrect.")
            return render(request, 'change_password.html')

    return render(request,"Change_password.html")


