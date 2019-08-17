import pytest

from app.services.round_service import (
    RoundTabulation,
    LEAVE_COMMENT,
    CALL_IPHONE,
    DISLIKE,
    GO_LIVE,
)
from app.services import round_service
from app.models import Move


@pytest.mark.django_db
def test_initializing_round(rnd):
    assert RoundTabulation(rnd).round == rnd


@pytest.mark.django_db
def test_move_population(game, rnd, p_1, p_2, p_3, p_4, p_5, move_factory):
    move_factory(round=rnd, action_type=LEAVE_COMMENT, player=p_3, victim=p_2)
    move_factory(round=rnd, action_type=LEAVE_COMMENT, player=p_5, victim=p_2)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_1, victim=p_2)
    move_factory(round=rnd, action_type=DISLIKE, player=p_2, victim=p_2)
    tab = RoundTabulation(rnd).populate_arrays_with_player_moves()
    assert tab[2] == {
        "leave_comment": [p_5.user.username, p_3.user.username],
        "dislike": [p_2.user.username],
        "call_iphone": [p_1.user.username],
    }
    assert tab[4] == {"leave_comment": [], "dislike": [], "call_iphone": []}
    assert Move.objects.all().count() == 5


@pytest.mark.django_db
def test_go_live_with_call(rnd, p_1, p_2, p_3, p_4, p_5, move_factory):
    """message was created, points are corrected, player is removed from player points array"""
    move_factory(round=rnd, action_type=GO_LIVE, player=p_1)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_2, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
