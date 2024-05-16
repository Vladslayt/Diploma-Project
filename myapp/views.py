import requests
from django.contrib.auth import login
from django.http import HttpResponse
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
def list_lobby_view(request, lobby_id=0):
    all_lobbies = Lobby.objects.all()
    user_lobbies = request.user.joined_lobbies.all()

    if request.method == 'POST':
        if 'join_lobby' in request.POST:
            lobby = get_object_or_404(Lobby, id=lobby_id)
            if lobby.members.count() < lobby.max_people:
                return lobby_detail_view(request, lobby_id)
        if 'delete_lobby' in request.POST:
            lobby_id = request.POST.get('lobby_id')
            lobby = get_object_or_404(Lobby, id=lobby_id)
            lobby.delete()
            return redirect('list-lobby')
        else:
            form = LobbyForm(request.POST)
            if form.is_valid():
                new_lobby = form.save(commit=False)
                new_lobby.owner = request.user
                new_lobby.save()
                new_lobby.members.add(request.user)
                return redirect('list-lobby')
    else:
        form = LobbyForm()
    return render(request, 'listlobby.html', {'all_lobbies': all_lobbies, 'user_lobbies': user_lobbies, 'form': form})


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

    return render(request, 'lobby_detail.html', {
        'lobby': lobby,
        'flats_all': flats_all,
        'flats': flats,
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