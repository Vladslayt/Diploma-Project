import requests
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from rest_framework import viewsets
from .forms import LobbyForm, RegisterForm, ProfileForm
from .models import Lobby, Flat, Profile
from .serializers import LobbySerializer, FlatSerializer
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


@login_required
def list_lobby_view(request):
    all_lobbies = Lobby.objects.all()
    user_lobbies = request.user.joined_lobbies.all()
    form = LobbyForm()
    if request.method == 'POST':
        if 'join_lobby' in request.POST:
            lobby_id = request.POST.get('lobby_id')
            lobby = get_object_or_404(Lobby, id=lobby_id)
            if lobby.members.filter(id=request.user.id).exists():
                return lobby_detail_view(request, lobby_id)

            elif lobby.members.count() < lobby.max_people:
                if not lobby.members.filter(id=request.user.id).exists():
                    lobby.members.add(request.user)
                return lobby_detail_view(request, lobby_id)

            else:
                return render(request, 'listlobby.html', {
                    'all_lobbies': all_lobbies,
                    'user_lobbies': user_lobbies,
                    'form': form,
                    'show_modal': True,
                    'modal_message': 'Лобби уже переполнено!'
                })
        elif 'delete_lobby' in request.POST:
            lobby_id = request.POST.get('lobby_id')
            lobby = get_object_or_404(Lobby, id=lobby_id)
            lobby.delete()
            return render(request, 'listlobby.html', {
                'all_lobbies': all_lobbies,
                'user_lobbies': user_lobbies,
                'form': form,
                'show_modal': False
            })

        else:
            form = LobbyForm(request.POST)
            if form.is_valid():
                new_lobby = form.save(commit=False)
                new_lobby.owner = request.user
                new_lobby.save()
                new_lobby.members.add(request.user)
                return render(request, 'listlobby.html', {
                    'all_lobbies': all_lobbies,
                    'user_lobbies': user_lobbies,
                    'form': form,
                    'show_modal': False
                })

    else:
        form = LobbyForm()
    return render(request, 'listlobby.html', {
        'all_lobbies': all_lobbies,
        'user_lobbies': user_lobbies,
        'form': form,
        'show_modal': False
    })


# def list_lobby_view(request):
#     if request.method == 'POST' and 'delete_lobby' in request.POST:
#         lobby_id = request.POST.get('lobby_id')
#         lobby = get_object_or_404(Lobby, id=lobby_id)
#         lobby.delete()
#         return redirect('list-lobby')
#     elif request.method == 'POST':
#         form = LobbyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('list-lobby')
#     else:
#         form = LobbyForm()
#     lobbies = Lobby.objects.all()
#     return render(request, 'listlobby.html', {'lobbies': lobbies, 'form': form})


@login_required
def lobby_detail_view(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    flats = lobby.flats.all()
    flats_all = request.session.get('flats_all')
    submitted = request.session.get('submitted', False)

    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')
    rooms = request.POST.get('rooms')
    region = request.POST.get('region', '')
    district = request.POST.get('district')
    underground = request.POST.get('underground', '')

    if request.method == 'POST':
        if 'add_flat' in request.POST:
            link = request.POST.get('flat_link')
            price = request.POST.get('flat_price')
            # Проверка на существование квартиры с таким же link в этом лобби
            if not Flat.objects.filter(link=link, lobby=lobby).exists():
                Flat.objects.create(link=link, price_per_month=price, lobby=lobby)
        elif 'remove_flat' in request.POST:
            flat_id = request.POST.get('flat_id')
            flat = get_object_or_404(Flat, id=flat_id)
            flat.delete()
        else:
            submitted = True
            url = "http://localhost:8000/api/v1/flats"
            headers = {
                'Authorization': 'Basic ' + 'dXNlcjoxMjM0',  # Base64-encoded 'user:1234'
                'Content-Type': 'application/json',
            }
            params = {}
            if min_price:
                params['min_price'] = min_price
            if max_price:
                params['max_price'] = max_price
            if rooms:
                params['rooms'] = rooms
            if region:
                params['region'] = region
            if district:
                params['district'] = district
            if underground:
                params['underground'] = underground

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                flats_all = response.json()
                request.session['flats_all'] = flats_all
                request.session['submitted'] = submitted
            else:
                return HttpResponse('Failed to fetch data', status=500)

            if flats_all == "No flats found":
                flats_all = None
                request.session['flats_all'] = flats_all
                request.session['submitted'] = submitted

        flats = lobby.flats.all()

    # Pagination for flats_all
    flats_all_paginator = Paginator(flats_all, 5)  # Show 5 flats per page
    flats_all_page_number = request.GET.get('page_all')
    flats_all_page_obj = flats_all_paginator.get_page(flats_all_page_number)

    # Pagination for selected flats
    flats_paginator = Paginator(flats, 5)  # Show 5 flats per page
    flats_page_number = request.GET.get('page_selected')
    flats_page_obj = flats_paginator.get_page(flats_page_number)

    return render(request, 'lobby_detail.html', {
        'lobby': lobby,
        'flats_all': flats_all_page_obj,
        'flats': flats_page_obj,
        'submitted': submitted,
        'min_price': min_price,
        'max_price': max_price,
        'rooms': rooms,
        'region': region,
        'district': district,
        'underground': underground,
    })


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile.html', {'form': form})


def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')


class LobbyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer


class FlatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer


def add_flat(request):
    if request.method == 'POST':
        lobby_id = request.POST.get('lobby_id')
        lobby = get_object_or_404(Lobby, id=lobby_id)
        link = request.POST.get('flat_link')
        price = request.POST.get('flat_price')
        if not Flat.objects.filter(link=link, lobby=lobby).exists():
            Flat.objects.create(link=link, price_per_month=price, lobby=lobby)
        return redirect('lobby-detail', lobby_id=lobby.id)


def remove_flat(request):
    if request.method == 'POST':
        flat_id = request.POST.get('flat_id')
        flat = get_object_or_404(Flat, id=flat_id)
        lobby_id = flat.lobby.id
        flat.delete()
        return redirect('lobby-detail', lobby_id=lobby_id)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        return reverse_lazy('list-lobby')


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'registration/register.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list-lobby')
        return render(request, self.template_name, {'form': form})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list-lobby')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
