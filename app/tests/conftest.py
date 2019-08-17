import pytest
from pytest_factoryboy import register

from .factories import (
    UserFactory,
    GameFactory,
    GamePlayerFactory,
    MoveFactory,
    RoundFactory,
)

register(UserFactory)
register(GameFactory)
register(GamePlayerFactory)
register(MoveFactory)
register(RoundFactory)


@pytest.fixture()
def game(game_factory):
    return game_factory()


@pytest.fixture()
def rnd(game, round_factory):
    return round_factory(game=game, started=True)


@pytest.fixture()
def p_1(game, user_factory, game_player_factory):
    return game_player_factory(game=game, user=user_factory(), started=True)


@pytest.fixture()
def p_2(game, user_factory, game_player_factory):
    return game_player_factory(game=game, user=user_factory(), started=True)


@pytest.fixture()
def p_3(game, user_factory, game_player_factory):
    return game_player_factory(game=game, user=user_factory(), started=True)


@pytest.fixture()
def p_4(game, user_factory, game_player_factory):
    return game_player_factory(game=game, user=user_factory(), started=True)


@pytest.fixture()
def p_5(game, user_factory, game_player_factory):
    return game_player_factory(game=game, user=user_factory(), started=True)


@pytest.fixture()
def p_6(game, user_factory, game_player_factory):
    return game_player_factory(game=game, user=user_factory(), started=True)
