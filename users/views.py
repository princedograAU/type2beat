from django.shortcuts import render,redirect
from django.contrib import messages
from users.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, logout as auth_logout, login as auth_login

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form':form})

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request,'Invalid Username or Password')
            return redirect('login')
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'form':LoginForm()})


def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
        return render(request, 'logout.html')
    else:
        return redirect('login')
