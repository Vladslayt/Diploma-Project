import requests
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from .models import User
from rest_framework import viewsets
from .forms import LobbyForm, ProfileForm
from .models import Lobby, Flat, Profile, Rating
from .serializers import LobbySerializer, FlatSerializer
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required


@login_required
def list_lobby_view(request):
    all_lobbies = Lobby.objects.all()
    user_lobbies = request.user.joined_lobbies.all()
    form = LobbyForm(request.POST or None)

    filter_name = request.GET.get('filter_name')
    filter_max_people = request.GET.get('filter_max_people')
    filter_is_private = request.GET.get('filter_is_private')
    filter_lobby_type = request.GET.get('filter_lobby_type')

    if filter_name:
        all_lobbies = all_lobbies.filter(name__icontains=filter_name)
    if filter_max_people:
        all_lobbies = all_lobbies.filter(max_people=filter_max_people)
    if filter_is_private:
        if filter_is_private == "true":
            all_lobbies = all_lobbies.filter(is_private=True)
        elif filter_is_private == "false":
            all_lobbies = all_lobbies.filter(is_private=False)
    if filter_lobby_type:
        all_lobbies = all_lobbies.filter(lobby_type=filter_lobby_type)

    if request.method == 'POST':
        if 'join_lobby' in request.POST:
            lobby_id = request.POST.get('lobby_id')
            lobby = get_object_or_404(Lobby, id=lobby_id)

            if lobby.is_private:
                password = request.POST.get('password')
                if lobby.password == password:
                    if not lobby.members.filter(id=request.user.id).exists():
                        lobby.members.add(request.user)
                    return redirect('lobby-detail', lobby_id=lobby_id)
                else:
                    return render(request, 'listlobby.html', {
                        'all_lobbies': all_lobbies,
                        'user_lobbies': user_lobbies,
                        'form': form,
                        'show_modal': True,
                        'modal_message': 'Неверный пароль!'
                    })

            if lobby.members.filter(id=request.user.id).exists():
                return redirect('lobby-detail', lobby_id=lobby_id)
            elif lobby.members.count() < lobby.max_people:
                if not lobby.members.filter(id=request.user.id).exists():
                    lobby.members.add(request.user)
                    return redirect('lobby-detail', lobby_id=lobby_id)
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
            return redirect('list-lobby')

        elif 'create_lobby' in request.POST:
            name = request.POST.get('name')
            max_people = request.POST.get('max_people')
            is_private = 'is_private' in request.POST
            password = request.POST.get('password') if is_private else None
            lobby_type = request.POST.get('lobby_type')
            description = request.POST.get('description')

            if not name or not max_people or (is_private and not password):
                messages.error(request, 'Заполните все обязательные поля.')
                return redirect('list-lobby')

            new_lobby = Lobby.objects.create(
                name=name,
                max_people=max_people,
                is_private=is_private,
                password=password,
                lobby_type=lobby_type,
                owner=request.user,
                description=description,
            )
            new_lobby.members.add(request.user)
            return redirect('list-lobby')

    return render(request, 'listlobby.html', {
        'all_lobbies': all_lobbies,
        'user_lobbies': user_lobbies,
        'show_modal': False
    })


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

    price_per_m2_coeff = request.POST.get('price_per_m2_coeff')
    common_ecology_coeff = request.POST.get('common_ecology_coeff')
    population_density_coeff = request.POST.get('population_density_coeff')
    green_spaces_coeff = request.POST.get('green_spaces_coeff')
    negative_impact_coeff = request.POST.get('negative_impact_coeff')
    phone_nets_coeff = request.POST.get('phone_nets_coeff')
    crime_coeff = request.POST.get('crime_coeff')

    if request.method == 'POST':
        if 'add_flat' in request.POST:
            link = request.POST.get('flat_link')
            price = request.POST.get('flat_price')
            if not Flat.objects.filter(link=link, lobby=lobby).exists():
                Flat.objects.create(link=link, price_per_month=price, lobby=lobby)
            else:
                request.session['show_modal'] = True
                request.session['modal_message'] = 'Квартира уже добавлена!'
                return redirect('lobby-detail', lobby_id=lobby_id)
        elif 'remove_flat' in request.POST:
            flat_link = request.POST.get('flat_link')
            flat = get_object_or_404(Flat, link=flat_link)
            flat.delete()
        elif 'rate_flat' in request.POST:
            flat_link = request.POST.get('flat_link')
            score = int(request.POST.get('score'))
            flat = get_object_or_404(Flat, link=flat_link)
            rating, created = Rating.objects.update_or_create(
                flat=flat, user=request.user, defaults={'score': score}
            )
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
            if price_per_m2_coeff:
                params['price_per_m2_coeff'] = price_per_m2_coeff
            if common_ecology_coeff:
                params['common_ecology_coeff'] = common_ecology_coeff
            if population_density_coeff:
                params['population_density_coeff'] = population_density_coeff
            if green_spaces_coeff:
                params['green_spaces_coeff'] = green_spaces_coeff
            if negative_impact_coeff:
                params['negative_impact_coeff'] = negative_impact_coeff
            if phone_nets_coeff:
                params['phone_nets_coeff'] = phone_nets_coeff
            if crime_coeff:
                params['crime_coeff'] = crime_coeff

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                flats_all = response.json()
                if flats_all == 'No flats found':
                    flats_all = None

                request.session['flats_all'] = flats_all
                request.session['submitted'] = submitted
            else:
                return HttpResponse('Failed to fetch data', status=500)

        flats = lobby.flats.all()

    # # Pagination for selected flats
    # flats_paginator = Paginator(flats, 5)  # Show 5 flats per page
    # flats_page_number = request.GET.get('page_selected')
    # flats_page_obj = flats_paginator.get_page(flats_page_number)
    show_modal = request.session.pop('show_modal', False)
    modal_message = request.session.pop('modal_message', '')

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
        'price_per_m2_coeff': price_per_m2_coeff,
        'common_ecology_coeff': common_ecology_coeff,
        'population_density_coeff': population_density_coeff,
        'green_spaces_coeff': green_spaces_coeff,
        'negative_impact_coeff': negative_impact_coeff,
        'phone_nets_coeff': phone_nets_coeff,
        'crime_coeff': crime_coeff,
        'show_modal': show_modal,
        'modal_message': modal_message,
    })


@login_required
def profile_view(request):
    # Ensure the profile exists
    profile, created = Profile.objects.get_or_create(user=request.user)
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile.html', {'user': user, 'form': form})


class UserProfileView(View):
    def get(self, request, pk):
        profile = get_object_or_404(Profile, user_id=pk)
        return render(request, 'user_profile.html', {'profile': profile})


def privacy_policy_view(request):
    return render(request, 'privacy_policy.html')


class LobbyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lobby.objects.all()
    serializer_class = LobbySerializer


class FlatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Flat.objects.all()
    serializer_class = FlatSerializer


# def add_flat(request):
#     if request.method == 'POST':
#         lobby_id = request.POST.get('lobby_id')
#         lobby = get_object_or_404(Lobby, id=lobby_id)
#         link = request.POST.get('flat_link')
#         price = request.POST.get('flat_price')
#         if not Flat.objects.filter(link=link, lobby=lobby).exists():
#             Flat.objects.create(link=link, price_per_month=price, lobby=lobby)
#
#         page_selected = ""
#         if request.POST.get("page_selected") is not None:
#             page_selected = "page_selected=" + request.POST.get("page_selected")
#
#         redirect_url = reverse('lobby-detail', args=[lobby.id])
#         if page_selected != "":
#             redirect_url = f"{redirect_url}?{page_selected}"
#
#         return redirect(redirect_url)


# def remove_flat(request):
#     if request.method == 'POST':
#         flat_id = request.POST.get('flat_id')
#         flat = get_object_or_404(Flat, id=flat_id)
#         lobby_id = flat.lobby.id
#         flat.delete()
#
#         page_selected = ""
#         if request.POST.get("page_selected") is not None:
#             page_selected = "page_selected=" + request.POST.get("page_selected")
#
#         redirect_url = reverse('lobby-detail', args=[lobby_id])
#         if page_selected != "":
#             redirect_url = f"{redirect_url}?{page_selected}"
#
#         return redirect(redirect_url)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_redirect_url(self):
        redirect_to = self.request.GET.get('next', self.get_success_url())
        return redirect_to

    def get_success_url(self):
        return reverse_lazy('list-lobby')


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
