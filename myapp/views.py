import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets
from .models import Lobby, Flat
from .serializers import LobbySerializer, FlatSerializer


def search_apartments(request):
    flats = None
    submitted = False
    min_price = request.POST.get('min_price')
    max_price = request.POST.get('max_price')
    rooms = request.POST.get('rooms')
    region = request.POST.get('region', '')
    district = request.POST.get('district')
    underground = request.POST.get('underground', '')

    if request.method == 'POST':
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
            flats = response.json()
        else:
            return HttpResponse('Failed to fetch data', status=500)

        if flats == "No flats fount":
            flats = None
    return render(request, 'lobby.html', {
        'flats': flats,
        'submitted': submitted,
        'min_price': min_price,
        'max_price': max_price,
        'rooms': rooms,
        'region': region,
        'district': district,
        'underground': underground,
    })


def listlobby(request):
    return render(request, 'listlobby.html')


def lobby(request):
    return render(request, 'lobby.html')


class LobbyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer


class FlatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer
