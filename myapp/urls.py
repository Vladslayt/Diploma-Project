"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import LobbyViewSet, FlatViewSet, CustomLoginView

router = DefaultRouter()
router.register(r'lobby', LobbyViewSet)
router.register(r'Flat', FlatViewSet)

urlpatterns = [
    path('', views.list_lobby_view, name='list-lobby'),
    path('lobby/<int:lobby_id>/', views.lobby_detail_view, name='lobby-detail'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('accounts/register/', views.register_view, name='register'),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('privacy_policy/', views.privacy_policy_view, name='privacy_policy'),
]
