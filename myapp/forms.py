from django import forms
from .models import Lobby


class LobbyForm(forms.ModelForm):
    class Meta:
        model = Lobby
        fields = ['name', 'max_people', 'is_private', 'lobby_type']
