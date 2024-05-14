import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from rest_framework import viewsets

from .forms import LobbyForm
from .models import Lobby, Flat
from .serializers import LobbySerializer, FlatSerializer


def list_lobby_view(request):
    if request.method == 'POST' and 'delete_lobby' in request.POST:
        lobby_id = request.POST.get('lobby_id')
        lobby = get_object_or_404(Lobby, id=lobby_id)
        lobby.delete()
        return redirect('list-lobby')
    elif request.method == 'POST':
        form = LobbyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list-lobby')
    else:
        form = LobbyForm()
    lobbies = Lobby.objects.all()
    return render(request, 'listlobby.html', {'lobbies': lobbies, 'form': form})


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

        flats = lobby.flats.all()  # Обновление списка квартир после добавления или удаления

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