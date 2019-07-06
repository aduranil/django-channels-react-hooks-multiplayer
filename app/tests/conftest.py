import pytest
from pytest_factoryboy import register

from .factories import UserFactory, GameFactory, GamePlayerFactory, MoveFactory, RoundFactory

register(UserFactory)
register(GameFactory)
register(GamePlayerFactory)
register(MoveFactory)
register(RoundFactory)


@pytest.fixture
def setup_3player_game(user_factory, game_factory, game_player_factory):
    game = game_factory()
    user1 = user_factory()
    user2 = user_factory()
    user3 = user_factory()
    game_player_factory(game=game, user=user1)
    game_player_factory(game=game, user=user2)
    game_player_factory(game=game, user=user3)
    return game
