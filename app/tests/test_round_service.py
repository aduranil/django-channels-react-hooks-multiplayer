import pytest

from app.services.round_service import (
    RoundTabulation,
    LEAVE_COMMENT,
    CALL_IPHONE,
    DISLIKE,
    GO_LIVE,
    POST_SELFIE,
    DONT_POST,
    NO_MOVE,
    DISLIKE_DM,
)
from app.services import round_service, message_service
from app.models import Move, Message, GamePlayer


def message(game, username):
    return Message.objects.get(game=game, username=username).message

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
    """message was created, points are corrected, player is removed from player
    points array, they have one less story"""
    move = move_factory(round=rnd, action_type=GO_LIVE, player=p_1, victim=None)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_2, victim=p_1)
    move_factory(round=rnd, action_type=DISLIKE, player=p_3, victim=p_1)
    move_factory(round=rnd, action_type=DISLIKE, player=p_4, victim=p_1)
    move_factory(round=rnd, action_type=LEAVE_COMMENT, player=p_5, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.iphone_msg(move, [p_2.user.username])
    p_1 = GamePlayer.objects.get(id=p_1.id)
    assert p_1.go_live == 1
    assert tab[p_1.id] == -50

@pytest.mark.django_db
def test_dont_post_twice(game, rnd, p_1, move_factory, round_factory):
    previous_round = round_factory(game=game, started=False)
    move_factory(round=previous_round, action_type=DONT_POST, victim=None, player=p_1)
    move = move_factory(round=rnd, action_type=DONT_POST, victim=None, player=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.dont_post_msg(move, True)
    assert tab[p_1.id] == -10

@pytest.mark.django_db
def test_dont_post_twice_with_danger(game, rnd, p_1, p_2, move_factory, round_factory):
    previous_round = round_factory(game=game, started=False)
    move_factory(round=previous_round, action_type=DONT_POST, victim=None, player=p_1)
    move = move_factory(round=rnd, action_type=DONT_POST, victim=None, player=p_1)
    move_factory(round=rnd, action_type=GO_LIVE, player=p_2, victim=None)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.dont_post_msg(move, True)
    assert tab[p_1.id] == 0

@pytest.mark.django_db
def test_dont_post_once(rnd, p_1, move_factory):
    move = move_factory(round=rnd, action_type=DONT_POST, victim=None, player=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.dont_post_msg(move, False)
    assert tab[p_1.id] == 0

@pytest.mark.django_db
def test_dont_post_dislike(rnd, p_1, p_2, p_3, move_factory):
    move = move_factory(round=rnd, action_type=DONT_POST, victim=None, player=p_1)
    move_factory(round=rnd, action_type=DISLIKE, player=p_2, victim=p_1)
    move_factory(round=rnd, action_type=DISLIKE, player=p_3, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.dont_post_msg(move, False)
    assert tab[p_1.id] == 2 * DISLIKE_DM
