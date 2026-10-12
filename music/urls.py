from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login"),
    path("register/", views.register_page, name="register"),
    path("search/", views.search, name="search"),
    path("trending/", views.trending, name="trending"),
    path("liked/", views.liked_songs, name="liked"),
    path("playlists/", views.playlists, name="playlists"),
    path("playlists/<int:pk>/", views.playlist_detail, name="playlist_detail"),
    path("play/<int:pk>/", views.player, name="player"),
    path("account/", views.account, name="account"),
    path("account/recent/", views.recent, name="recent"),
    path("account/settings/", views.settings_page, name="settings"),
]
