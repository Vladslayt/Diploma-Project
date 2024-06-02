import requests
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db.models import Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from rest_framework import viewsets
from .forms import LobbyForm, ProfileForm, RegisterForm
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

    filters = {
        'name__icontains': request.GET.get('filter_name'),
        'max_people': request.GET.get('filter_max_people'),
        'is_private': {'true': True, 'false': False}.get(request.GET.get('filter_is_private')),
        'lobby_type': request.GET.get('filter_lobby_type')
    }
    filters = {k: v for k, v in filters.items() if v}

    if filters:
        all_lobbies = all_lobbies.filter(**filters)

    if request.method == 'POST':
        if 'join_lobby' in request.POST:
            lobby_id = request.POST.get('lobby_id')
            lobby = get_object_or_404(Lobby, id=lobby_id)
            profile = request.user.profile

            if lobby.lobby_type in ['male', 'female'] and profile.gender != lobby.lobby_type:
                if lobby.lobby_type == 'male':
                    type_lobby = 'мужчины'
                else:
                    type_lobby = 'женщины'

                return render(request, 'listlobby.html', {
                    'all_lobbies': all_lobbies,
                    'user_lobbies': user_lobbies,
                    'form': form,
                    'show_modal': True,
                    'modal_message': f'В это лобби могут заходить только {type_lobby}.'
                })

            if lobby.members.filter(id=request.user.id).exists():
                return redirect('lobby-detail', lobby_id=lobby_id)

            if lobby.members.count() >= lobby.max_people:
                return render(request, 'listlobby.html', {
                    'all_lobbies': all_lobbies,
                    'user_lobbies': user_lobbies,
                    'form': form,
                    'show_modal': True,
                    'modal_message': 'Лобби уже переполнено!'
                })

            if lobby.is_private and lobby.password != request.POST.get('password'):
                return render(request, 'listlobby.html', {
                    'all_lobbies': all_lobbies,
                    'user_lobbies': user_lobbies,
                    'form': form,
                    'show_modal': True,
                    'modal_message': 'Неверный пароль!'
                })

            lobby.members.add(request.user)
            return redirect('lobby-detail', lobby_id=lobby_id)

        elif 'delete_lobby' in request.POST:
            lobby_id = request.POST.get('lobby_id')
            lobby = get_object_or_404(Lobby, id=lobby_id)
            lobby.delete()
            return redirect('list-lobby')

        elif 'leave_lobby' in request.POST:
            lobby_id = request.POST.get('lobby_id')
            lobby = get_object_or_404(Lobby, id=lobby_id)
            lobby.members.remove(request.user)
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
def edit_lobby_view(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)

    if request.user != lobby.owner:
        return redirect('lobby-detail', lobby_id=lobby_id)

    if request.method == 'POST':
        if 'remove_member' in request.POST:
            member_id = request.POST.get('member_id')
            member = get_object_or_404(User, id=member_id)
            if member != request.user:
                lobby.members.remove(member)
            return redirect('edit-lobby', lobby_id=lobby_id)

        name = request.POST.get('name')
        max_people = int(request.POST.get('max_people'))
        is_private = 'is_private' in request.POST
        password = request.POST.get('password') if is_private else ''
        lobby_type = request.POST.get('lobby_type')
        description = request.POST.get('description')

        errors = []

        if max_people < lobby.members.count():
            errors.append(
                f"Максимальное количество участников не может быть меньше текущего числа участников ({lobby.members.count()}).")

        if is_private and not password:
            errors.append("Приватное лобби должно иметь пароль.")

        if errors:
            return render(request, 'edit_lobby.html', {
                'lobby': lobby,
                'members': lobby.members.all(),
                'errors': errors,
                'form_data': {
                    'name': name,
                    'max_people': max_people,
                    'is_private': is_private,
                    'password': password,
                    'lobby_type': lobby_type,
                    'description': description,
                }
            })

        lobby.name = name
        lobby.max_people = max_people
        lobby.is_private = is_private
        lobby.password = password
        lobby.lobby_type = lobby_type
        lobby.description = description
        lobby.save()
        return redirect('list-lobby')

    members = lobby.members.all()
    return render(request, 'edit_lobby.html', {'lobby': lobby, 'members': members})


@login_required
def lobby_detail_view(request, lobby_id):
    lobby = get_object_or_404(Lobby, id=lobby_id)
    flats = lobby.flats.annotate(average_rating=Avg('ratings__score')).order_by('-average_rating')
    flats_all = request.session.get('flats_all')
    submitted = request.session.get('submitted', False)

    filter_params = {
        'min_price': request.POST.get('min_price'),
        'max_price': request.POST.get('max_price'),
        'rooms': request.POST.get('rooms'),
        'region': request.POST.get('region', ''),
        'district': request.POST.get('district'),
        'underground': request.POST.get('underground', ''),
        'price_per_m2_coeff': request.POST.get('price_per_m2_coeff'),
        'common_ecology_coeff': request.POST.get('common_ecology_coeff'),
        'population_density_coeff': request.POST.get('population_density_coeff'),
        'green_spaces_coeff': request.POST.get('green_spaces_coeff'),
        'negative_impact_coeff': request.POST.get('negative_impact_coeff'),
        'phone_nets_coeff': request.POST.get('phone_nets_coeff'),
        'crime_coeff': request.POST.get('crime_coeff')
    }

    selected_fields = request.session.get('selected_fields', ['price', 'area'])

    if request.method == 'POST':
        if 'add_flat' in request.POST:
            flat_data = {
                'link': request.POST.get('flat_link'),
                'price_per_month': request.POST.get('flat_price'),
                'total_meters': request.POST.get('flat_total_meters'),
                'rooms': request.POST.get('flat_rooms'),
                'district': request.POST.get('flat_district'),
                'underground': request.POST.get('flat_underground')
            }
            if not Flat.objects.filter(link=flat_data['link'], lobby=lobby).exists():
                Flat.objects.create(lobby=lobby, **flat_data)
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
            Rating.objects.update_or_create(flat=flat, user=request.user, defaults={'score': score})
        elif 'fields' in request.POST:
            selected_fields = request.POST.getlist('fields')
            request.session['selected_fields'] = selected_fields
        else:
            submitted = True
            url = "http://localhost:8000/api/v1/flats"
            headers = {
                'Authorization': 'Basic ' + 'dXNlcjoxMjM0',  # Base64-encoded 'user:1234'
                'Content-Type': 'application/json',
            }
            params = {k: v for k, v in filter_params.items() if v}

            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                flats_all = response.json()
                if flats_all != 'No flats found':
                    flats_all = flats_all[:100]
                request.session['flats_all'] = flats_all
                request.session['submitted'] = submitted
            else:
                return HttpResponse('Failed to fetch data', status=500)

        flats = lobby.flats.annotate(average_rating=Avg('ratings__score')).order_by('-average_rating')

    show_modal = request.session.pop('show_modal', False)
    modal_message = request.session.pop('modal_message', '')

    return render(request, 'lobby_detail.html', {
        'lobby': lobby,
        'flats_all': flats_all,
        'flats': flats,
        'submitted': submitted,
        'selected_fields': selected_fields,
        **filter_params,
        'show_modal': show_modal,
        'modal_message': modal_message,
    })


@login_required
def profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    user = request.user
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
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


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

    def get_redirect_url(self):
        return self.request.GET.get('next', self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('list-lobby')


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list-lobby')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})
