from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver,Signal
from django.core.mail import send_mail
import random
from .models import *
from .forms import *


@receiver(user_logged_in)
def login_info(sender, request, user, **kwargs):
    name = user.first_name
    print(f'user {name} is successfully logged in')

@receiver(user_logged_out)
def logout_info(sender, request, user, **kwargs):
    name = user.first_name
    print(f'user {name} is successfully logged out')




@receiver(post_save,sender=UserProfile)
def send_mail_for_otp(sender,instance,created,**kwargs):
    if created:
        memail=instance.email
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
        
def send_mail_sucessful_regestration(sender,instance,created,**kwargs):
   pass




password_changed = Signal()

@receiver(password_changed)
def handle_password_change(sender, user, request, **kwargs):
    email=user.email
    print(f"🔒 Password changed for user: {user.first_name}")
    send_mail(
                'Password Change',
                f'The password of your account has been changed',
                'lokeshpatel2714@gmail.com',
                [email],
                fail_silently=True,
            )
    

reset_password=Signal()

@receiver(reset_password)
def send_mail_for_otp(sender,email,**kwargs):
        
        memail=email
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