from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Lobby, Message
from .forms import LobbyForm
from django.utils import timezone


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exist')

    context = {'page': page}
    return render(request, 'base/authorization.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'base/authorization.html', context)


def home(request):
    data = {}
    if request.user.is_authenticated:
        player = request.user.player
        data = {
            'wins': player.wins,
            'losses': player.losses,
            'draws': player.draws,
            'total_games': player.total_games,
            'rating': player.rating,
            'last_online': player.last_online,
            'current_lobby': player.current_lobby,
        }

    def get_lobby_data(lobby_queryset, status):
        lobby_data = []
        for lobby in lobby_queryset:
            lobby_members = lobby.members.all()
            lobby_data.append({
                'lobby': lobby,
                'members': lobby_members,
                'member_count': lobby_members.count(),
            })
        return {'lobby_data': lobby_data, f'{status}_lobbies': lobby_queryset}

    available_lobbies = Lobby.objects.filter(status='available')
    playing_lobbies = Lobby.objects.filter(status='playing')
    finished_lobbies = Lobby.objects.filter(status='finished')
    print(get_lobby_data(available_lobbies, 'available'))
    context = {
        'data': data,
        'lobbies': Lobby.objects.all(),
        'lobby_count': Lobby.objects.count(),
        **get_lobby_data(available_lobbies, 'available'),
        **get_lobby_data(playing_lobbies, 'playing'),
        **get_lobby_data(finished_lobbies, 'finished'),
    }
    return render(request, 'base/home.html', context)


def lobby(request, pk):
    lobby = Lobby.objects.get(id=pk)
    lobby_messages = lobby.message_set.all().order_by('-created_at')
    members = lobby.members.all()
    # if request.method == 'POST':
    #     lobby_message = Message.objects.create(
    #         author=request.user,
    #         lobby=lobby,
    #         content=request.POST.get('content')
    #     )
    #     lobby.members.add(request.user)
    #     return redirect('lobby', pk=lobby.id)
    all_ready = all(member.user.player.is_ready for member in members)
    if request.method == 'POST':
        player = request.user.player
        for player in members:
            player.is_ready = not player.is_ready
            player.save()

            all_ready = all(member.user.player.is_ready for member in members)
            if all_ready:
                return redirect('lobby', pk=lobby.id)
    context = {
        'lobby': lobby,
        'lobby_messages': lobby_messages,
        'members': members,
        'all_ready': all_ready,
    }
    return render(request, 'base/lobby.html', context)


@login_required(login_url='login')
def create_lobby(request):
    if request.method == 'POST':
        form = LobbyForm(request.POST)
        if form.is_valid():
            lobby = form.save(commit=False)
            lobby.host = request.user.player
            lobby.status = 'available'
            lobby.created_at = timezone.now()
            lobby.save()
            lobby.members.add(request.user.player)
            return redirect('lobby', pk=lobby.id)
    else:
        form = LobbyForm()

    context = {'form': form}
    return render(request, 'base/create_lobby.html', context)

@login_required(login_url='login')
def update_lobby(request, pk):
    lobby = Lobby.objects.get(id=pk)
    form = LobbyForm(instance=lobby)

    if request.user != lobby.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        form = LobbyForm(request.POST, instance=lobby)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/create_lobby.html', context)


@login_required(login_url='login')
def delete_lobby(request, pk):
    lobby = Lobby.objects.get(id=pk)
    if request.method == 'POST':
        lobby.delete()
        return redirect('home')
    context = {'obj': lobby}
    return render(request, 'base/delete_lobby.html', context)
