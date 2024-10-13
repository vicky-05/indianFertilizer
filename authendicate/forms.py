from django.contrib.auth.forms import UserCreationForm
from authendicate.models import User
from django import forms

class RegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Username'
        }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Email Address'
        }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Password'
        }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Confirm Password'
        }))
   
    class Meta:
        model = User
        fields = [ 'username', 'email', 'password1', 'password2' ]



class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Enter your email', max_length=100, required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
    }))
    otp = forms.CharField(label='Enter OTP', max_length=6, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter OTP',
    }))