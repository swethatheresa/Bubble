from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('signin')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            #return redirect('home')
            return HttpResponse('success')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {}
    return render(request, 'signin.html', context)

def logoutUser(request):
    logout(request)
    return redirect('signin')


def sign_up(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save_m2m()
            login(request, user)
            return redirect('signin')
            
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'signup.html', {'form': form})