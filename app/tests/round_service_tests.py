import pytest

from app.services.round_service import RoundTabulation

@pytest.mark.django_db
def test_initializing_round(rnd):
    assert RoundTabulation(rnd).round == rnd


def test_move_population(game, rnd, p_1, p_2, p_3, move_factory):
    move_factory(round=rnd, action_type="post_selfie", player=p_3)
    move_factory(round=rnd, action_type="post_selfie", player=p_2)
    tab = RoundTabulation(rnd).populate_arrays_with_player_moves()
