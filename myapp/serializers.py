from rest_framework import serializers
from .models import Lobby, Flat


class LobbySerializer(serializers.ModelSerializer):
    class Meta:
        model = Lobby
        fields = ['id', 'name', 'max_people', 'is_private', 'lobby_type', 'description', 'owner']


class FlatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flat
        fields = ['id', 'name', 'price']
