from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Lobby, Profile


class LobbyForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput(), label="Пароль")

    class Meta:
        model = Lobby
        fields = ['name', 'max_people', 'is_private', 'lobby_type', 'description', 'password']

    def __init__(self, *args, **kwargs):
        self.lobby = kwargs.pop('instance', None)
        super(LobbyForm, self).__init__(*args, **kwargs)

    def clean_max_people(self):
        max_people = self.cleaned_data.get('max_people')
        if self.lobby and self.lobby.members.count() > max_people:
            raise forms.ValidationError(
                f"Максимальное количество участников не может быть меньше текущего числа участников ({self.lobby.members.count()})"
            )
        return max_people

    def clean(self):
        cleaned_data = super().clean()
        is_private = cleaned_data.get("is_private")
        password = cleaned_data.get("password")

        if is_private and not password:
            self.add_error('password', "Приватное лобби должно иметь пароль.")

        return cleaned_data


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Электронная почта")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Имя пользователя',
            'password1': 'Пароль',
            'password2': 'Подтвердите пароль',
        }

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Подтвердите пароль'
        self.fields['password2'].widget = forms.PasswordInput()  # Изменяем виджет для второго поля пароля

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот адрес электронной почты уже используется.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise ValidationError("Пароли не совпадают.")
        return password2


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'email', 'first_name', 'last_name', 'phone', 'bio', 'birth_date',
            'address', 'city', 'country', 'postal_code', 'gender', 'profile_picture'
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
