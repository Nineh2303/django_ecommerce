from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm
from django_countries.fields import CountryField
from .models import UserBase


class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label='Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(max_length=100, help_text='Required',
                             error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ['user_name', 'email']

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username is existed")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(" Passwords is not match. ")
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError(" Please use another Email, that is already taken")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].widget.attrs.update({'placeholder': 'User name'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email...'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repeat Password'})


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username...', 'id': 'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'placeholder': 'Password',
            'id': 'login-pwd'
        }
    ))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label='Account Email(can not be change)', max_length=200,
                             widget=forms.TextInput(
                                 attrs={'placeholder': 'Email', 'id': 'form-email', 'readonly': 'readonly'}))
    first_name = forms.CharField(label="First Name", min_length=4, max_length=50,
                                 widget=forms.TextInput(attrs={'placeholder': 'Firstname', 'id': 'form-firstname'}))
    # country = CountryField()

    class Meta:
        model = UserBase
        fields = ('email', 'first_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['email'].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'placeholder': 'Email', 'id': 'form-email'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        u = UserBase.objects.filter(email=email)
        if not u:
            raise forms.ValidationError(
                'Unfortunatly we can not find that email address'
            )
        return email


class PwdResetConfirmForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'New Password', 'id': 'form-newpass'}))
    new_password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Repeat Password', 'id': 'form-newpass2'}))
