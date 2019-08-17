import pytest

from app.services.round_service import RoundTabulation, LEAVE_COMMENT, CALL_IPHONE, DISLIKE
from app.models import Move

@pytest.mark.django_db
def test_initializing_round(rnd):
    assert RoundTabulation(rnd).round == rnd

@pytest.mark.django_db
def test_move_population(game, rnd, p_1, p_2, p_3, p_4, move_factory):
    move_factory(round=rnd, action_type=LEAVE_COMMENT, player=p_3, victim=p_2)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_1, victim=p_2)
    move_factory(round=rnd, action_type=DISLIKE, player=p_2, victim=p_2)
    tab = RoundTabulation(rnd).populate_arrays_with_player_moves()
    assert tab[2] == {'leave_comment': 1, 'dislike': 1, 'call_iphone': 1}
    assert Move.objects.all().count() == 4
