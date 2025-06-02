from django.shortcuts import render,redirect
from accounts.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages
from accounts.models import EmailOTP    
from django.contrib.auth import login,logout,update_session_auth_hash
from .utils import custom_authenticate
from django.contrib.auth.decorators import login_required
from .signals import password_changed , reset_password
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
            user=UserProfile.objects.get(email=email)
            status=user.is_active
            try:
                EOTP=EmailOTP.objects.get(email=email,otp_code=otp_code)
                if EOTP.is_expired():
                    messages.error(request, 'OTP expired. Please register again.')
                    return HttpResponseRedirect('/register')
                

                elif not status :  # if user is not active
                    user.is_active = True
                    user.save()
                    EOTP.delete()
                    send_mail(
                        'Registration Sucessful',
                        'Your registration is successful',
                        'lokeshpatel2714@gmail.com',
                        [email],
                        fail_silently=True,
                    )
                    return HttpResponseRedirect('/home')
                else:
                    return HttpResponseRedirect('/set-new-password')
                
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

            password_changed.send(sender=change_password, user=user, request=request)

            messages.success(request, "✅ Password changed successfully.")
            return redirect('home')
        else:
            messages.error(request, "❌ Old password is incorrect.")
            return render(request, 'change_password.html')

    return render(request,"Change_password.html")






def Reset_Password(request):
    EPRFO = ResetPassword()
    if request.method == 'POST':
        RPFO = ResetPassword(request.POST)
        if RPFO.is_valid():
            user_email = RPFO.cleaned_data['email']
            checkmail = UserProfile.objects.values_list('email', flat=True)

            if user_email in checkmail:
                reset_password.send(sender=None, email=user_email)
                return redirect('otp_verification')  
            else:
                messages.error(request, "User not found.")
    
    d = {'EPRFO': EPRFO}
    return render(request, 'reset_password.html', d)





def  set_new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "❌ Passwords do not match.")
            return render(request, 'set_new_password.html', {'email': email})

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            messages.error(request, "❌ No user found with that email.")
            return render(request, 'set_new_password.html')

        user.set_password(new_password)
        user.save()

        messages.success(request, "✅ Password has been reset. You can now log in.")
        return redirect('user_login')  # redirect to login page

    return render(request, 'set_new_password.html') 



def Profile(request):
    return render(request,'Profile.html')