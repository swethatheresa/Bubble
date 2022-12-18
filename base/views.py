from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
import pickle
from datetime import datetime,timedelta
import googleapiclient
import sys
import json

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

temp={"installed":{"client_id":"676601264874-fke3t7c0otbu3ds86rt63j2e1v4cgrkg.apps.googleusercontent.com","project_id":"tink-her-hack","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {}
    return render(request, 'signin.html', context)

def logoutUser(request):
    logout(request)
    return redirect('signin')

def home(request):
    rooms = Room.objects.filter(host=request.user)
    print(request.user)
    events=Event.objects.filter(user=request.user)
    print(events)
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    interests=request.user.fields_of_interests.all()
    if(q!=''):
        posts = Post.objects.filter(
            Q(topic__name__icontains=q) &
            Q(city__icontains=request.user.city)
        )
    else:
        posts = Post.objects.none()
        for interest in interests:
            posts |= Post.objects.filter(
                Q(topic__name__icontains=interest) &
                Q(city__icontains=request.user.city)
            )
        
    context = {'events':events,'posts':posts,'rooms':rooms}
    return render(request, 'home.html', context)

@login_required(login_url='signin')
def createPost(request):
    form = PostForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        new=Room.objects.create(
            host=request.user,
            topic=topic,
            name='TalkRoom For Workshop',
            description=request.POST.get('caption'),
        )
        Post.objects.create(
            host=request.user,
            topic=topic,
            caption=request.POST.get('caption'),
            image=request.FILES.get('image'),
            city=request.POST.get('city'),
            room_id=new.id
        )
        
        return redirect('home')
    context = {'form': form, 'topics': topics}
    return render(request, 'create-post.html', context)

def createSchedule(request):
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            form.user = request.user
            form.save_m2m()
            event.save()
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'schedule-event.html', {'form': form})


def sign_up(request):
    form = MyUserCreationForm()
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            form.username = user.email
            form.save_m2m()
            user.save()
            
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
    return render(request, 'signup.html', {'form': form})

def room(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    if(q==None):
        title='All'
    else:
        title=q

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:30]

    context = {'title':title,'rooms': rooms,'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'room.html', context)

@login_required(login_url='signin')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('room')

    context = {'form': form, 'topics': topics}
    return render(request, 'create-room.html', context)

@login_required(login_url='signin')
def join(request,pk):
    room=Room.objects.get(id=pk)
    room_messages = room.message_set.all()[0:50]
    participants = room.participants.all()
    room.participants.add(request.user)
    request.user.fields_of_interests.add(room.topic)
    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room_details', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants,}
    return render(request,'room-details.html',context)


def room_details(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()[0:50]
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room_details',pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants,}
    return render(request, 'room-details.html', context)