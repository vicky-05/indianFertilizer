from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from authendicate.models import User
from django import forms

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Username'
        }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Email Address'
        }))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your Password',
        }),
    )
   
    class Meta:
        model = User
        fields = [ 'username', 'email' ]

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(password)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        print(self.cleaned_data.get('password'))
        user.set_password(self.cleaned_data["password"])  # Hash password before saving
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
        }),
        required = True,
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
        }),
        required = True,
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValidationError('Username is required.')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise ValidationError('Password is required.')
        return password

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError({
                    'username' : 'Invaild Username.',
                    'password' : 'Invaild Password.',
                    })

        return cleaned_data


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label='Enter your email', max_length=100, required=False, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email',
    }))
    otp = forms.CharField(label='Enter OTP', max_length=6, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter OTP',
    }))