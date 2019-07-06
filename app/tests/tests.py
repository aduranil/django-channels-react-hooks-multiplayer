import pytest

from .factories import RoundFactory
from app.models import Move, Round, GamePlayer

@pytest.mark.django_db
def test_everyone_posts_a_selfie(
    game_factory,
    user_factory,
    game_player_factory,
    round_factory,
    move_factory
):

    game = game_factory()
    round = round_factory(game=game, started=True)
    users = [user_factory(), user_factory(), user_factory()]
    for user in users:
        gp = game_player_factory(game=game, user=user, started=True)
        move_factory(round=round, action_type=Move.POST_SELFIE, player=gp)

    round.tabulate_round()
    for user in users:
        assert GamePlayer.objects.get(user=user).followers == 5
