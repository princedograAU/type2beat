# from users.models import User
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

# class RegistrationForm(forms.Form):
#     first_name = forms.CharField(label='First Name*', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your First Name here'}))
#     last_name = forms.CharField(label='Last Name*', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your Last Name here'}))
#     username = forms.CharField(label='Username*', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'Enter your Username here'}))
#     password = forms.CharField(label='Password*', max_length=16, required=True, widget=forms.TextInput(attrs={'type':'password','placeholder':'Enter your Password here'}))
#     renter_password = forms.CharField(label='Re-enter Password*', max_length=16, widget=forms.TextInput(attrs={'type':'password','placeholder':'Re-Enter your Password here'}), required=True)
#     email = forms.EmailField(label='E-mail', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter your E-mail here'}))
#     contact = forms.CharField(label='Mobile', max_length=11, required=False, widget=forms.TextInput(attrs={'placeholder':'Enter your Mobile Number here'}))
#
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=28, required=True, widget=forms.TextInput(attrs={'placeholder':'email: janedoe@abc.com'}))
    username = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder':'username: janedoe'}))
    first_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder':'first name: jane'}))
    last_name = forms.CharField(max_length=20, required=True, widget=forms.TextInput(attrs={'placeholder':'lastname: doe'}))
    password1 = forms.CharField(label='Password', max_length=16, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label='Re-enter password', max_length=16, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='username*', max_length=50, required=True, widget=forms.TextInput(attrs={'placeholder':'username: janedoe'}))
    password = forms.CharField(label='password*', max_length=16, required=True, widget=forms.TextInput(attrs={'placeholder':'password: abc@123', 'type':'password'}))
