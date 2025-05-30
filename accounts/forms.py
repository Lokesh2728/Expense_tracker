from accounts .models import *
from django import forms


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['email','first_name','last_name','password']
        widgets={
            'password':forms.PasswordInput()
        }

class EmailOTPForm(forms.ModelForm):
    class Meta:
        model=EmailOTP
        fields=['email','otp_code']
        widgets={
            'otp_code':forms.TextInput(attrs={'placeholder':'Enter OTP'})
        }   

class UserLoginForm(forms.Form):
    email=forms.EmailField( widget=forms.EmailInput ( attrs={'placeholder':'Enter email'}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}))


class ResetPassword(forms.Form):
     email = forms.EmailField(
        label="Enter your registered email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        max_length=254
    )
    