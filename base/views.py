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
        #return redirect('home')
        return HttpResponse('success')

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
        print(form)
        if form.is_valid():
            print(form)
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            form.save_m2m()
            login(request, user)
            return HttpResponse('success')
            #return redirect('home')
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
        Q(room__topic__name__icontains=q))[0:3]

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
    room.participants.add(User)
    room_messages = room.message_set.all()
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
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    context={}
    return render(request, 'room.html', context)

def room_details(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    context={}
    return render(request, 'room.html', context)