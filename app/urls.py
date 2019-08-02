# chat/urls.py
from django.urls import path
from app.views.game_views import GameCreateView, GameListView, GameGetView
from app.views.account_views import CreateUser, GetUser, LoginUser

urlpatterns = [
    path("users/", CreateUser.as_view()),
    path("game/", GameCreateView.as_view()),
    path("game/<int:id>", GameGetView.as_view()),
    path("games/", GameListView.as_view()),
    path("user/", GetUser.as_view()),
    path("login/", LoginUser.as_view()),
]
