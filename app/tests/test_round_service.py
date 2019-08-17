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
    POST_SELFIE_PTS,
    POST_SELFIE_DM,
    GO_LIVE_DM,
    NO_MOVE_DM
)
from app.services import round_service, message_service
from app.models import Move, Message, GamePlayer


def message(game, username):
    return Message.objects.get(game=game, username=username).message


@pytest.mark.django_db
def test_three_go_lives_two_calls(rnd, p_1, p_2, p_3, p_4, p_5, move_factory):
    """one go live still gets through causing damage to everyone else"""
    move_factory(round=rnd, action_type=GO_LIVE, player=p_1, victim=None)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_2, victim=p_1)
    move_factory(round=rnd, action_type=GO_LIVE, player=p_3, victim=None)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_4, victim=p_3)
    move_factory(round=rnd, action_type=GO_LIVE, player=p_5, victim=None)
    tab = RoundTabulation(rnd).tabulate()
    assert tab[p_1.id] == GO_LIVE_DM
    assert tab[p_2.id] == GO_LIVE_DM
    assert tab[p_3.id] == GO_LIVE_DM
    assert tab[p_4.id] == GO_LIVE_DM
    assert tab[p_5.id] == 0


@pytest.mark.django_db
def test_two_players_grab_and_go_live(rnd, p_1, p_2, p_3, move_factory):
    move_factory(round=rnd, action_type=GO_LIVE, player=p_1, victim=None)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_2, victim=p_1)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_3, victim=p_2)
    tab = RoundTabulation(rnd).tabulate()
    assert tab[p_1.id] == 0
    assert tab[p_2.id] == GO_LIVE_DM
    assert tab[p_3.id] == GO_LIVE_DM


@pytest.mark.django_db
def test_iphone_go_live_do_selfie(rnd, p_1, p_2, p_3, move_factory):
    """if a girl calls a girl who is trying to take a selfie, she sustains go
    live damage"""
    move_factory(round=rnd, action_type=GO_LIVE, player=p_1, victim=None)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_2, victim=p_3)
    move_factory(round=rnd, action_type=POST_SELFIE, player=p_3, victim=None)
    tab = RoundTabulation(rnd).tabulate()
    assert tab[p_1.id] == 0
    assert tab[p_2.id] == GO_LIVE_DM
    assert tab[p_3.id] == GO_LIVE_DM


@pytest.mark.django_db
def test_go_live_with_call(rnd, p_1, p_2, p_3, p_4, p_5, move_factory):
    """message was created, points are corrected, player is removed from player
    points array, they have one less story"""
    move_factory(round=rnd, action_type=GO_LIVE, player=p_1, victim=None)
    move = move_factory(round=rnd, action_type=CALL_IPHONE, player=p_2, victim=p_1)
    move_factory(round=rnd, action_type=DISLIKE, player=p_3, victim=p_1)
    move_factory(round=rnd, action_type=DISLIKE, player=p_4, victim=p_1)
    move_factory(round=rnd, action_type=LEAVE_COMMENT, player=p_5, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_2.user.username) in message_service.iphone_msg(
        move, p_1.user.username
    )
    p_1 = GamePlayer.objects.get(id=p_1.id)
    assert p_1.go_live == 1
    assert tab[p_1.id] == -50


@pytest.mark.django_db
def test_dont_post_twice(game, rnd, p_1, move_factory, round_factory):
    previous_round = round_factory(game=game, started=False)
    move_factory(round=previous_round, action_type=DONT_POST, victim=None, player=p_1)
    move = move_factory(round=rnd, action_type=DONT_POST, victim=None, player=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.dont_post_msg(
        move, True
    )
    assert tab[p_1.id] == -10


@pytest.mark.django_db
def test_dont_post_twice_with_danger(game, rnd, p_1, p_2, move_factory, round_factory):
    previous_round = round_factory(game=game, started=False)
    move_factory(round=previous_round, action_type=DONT_POST, victim=None, player=p_1)
    move = move_factory(round=rnd, action_type=DONT_POST, victim=None, player=p_1)
    move_factory(round=rnd, action_type=GO_LIVE, player=p_2, victim=None)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.dont_post_msg(
        move, True
    )
    assert tab[p_1.id] == 0


@pytest.mark.django_db
def test_dont_post_once(rnd, p_1, move_factory):
    move = move_factory(round=rnd, action_type=DONT_POST, victim=None, player=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.dont_post_msg(
        move, False
    )
    assert tab[p_1.id] == 0


@pytest.mark.django_db
def test_dont_post_dislike(rnd, p_1, p_2, p_3, move_factory):
    move = move_factory(round=rnd, action_type=DONT_POST, victim=None, player=p_1)
    move_factory(round=rnd, action_type=DISLIKE, player=p_2, victim=p_1)
    move_factory(round=rnd, action_type=DISLIKE, player=p_3, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.dont_post_msg(
        move, False
    )
    assert tab[p_1.id] == 2 * DISLIKE_DM


@pytest.mark.django_db
def test_post_selfie_success(rnd, p_1, move_factory):
    """message was created, points are corrected, player is removed from player
    points array, they have one less story"""
    move = move_factory(round=rnd, action_type=POST_SELFIE, player=p_1, victim=None)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.post_selfie_msg(move, POST_SELFIE_PTS)
    p_1 = GamePlayer.objects.get(id=p_1.id)
    assert p_1.selfies == 2
    assert tab[p_1.id] == POST_SELFIE_PTS


@pytest.mark.django_db
def test_post_selfie_calls(rnd, p_1, p_2, move_factory):
    """message was created, points are corrected, player is removed from player
    points array, they have one less story"""
    move_factory(round=rnd, action_type=POST_SELFIE, player=p_1, victim=None)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_2, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert tab[p_1.id] == 0


@pytest.mark.django_db
def test_post_selfie_comments(rnd, p_1, p_2, move_factory):
    """message was created, points are corrected, player is removed from player
    points array, they have one less story"""
    move_factory(round=rnd, action_type=POST_SELFIE, player=p_1, victim=None)
    move_factory(round=rnd, action_type=LEAVE_COMMENT, player=p_2, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert tab[p_1.id] == POST_SELFIE_DM

@pytest.mark.django_db
def test_message_when_leave_comment_grabbed(rnd, p_1, p_2, p_3, move_factory):
    """make sure the right message appears if the user was grabbed by someone else"""
    move1 = move_factory(round=rnd, action_type=POST_SELFIE, player=p_1, victim=None)
    move2 = move_factory(round=rnd, action_type=LEAVE_COMMENT, player=p_2, victim=p_1)
    move_factory(round=rnd, action_type=CALL_IPHONE, player=p_3, victim=p_2)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.post_selfie_msg(move1, 20, False, False)
    assert message(rnd.game, p_2.user.username) in message_service.leave_comment_msg(move2, p_1.user.username, 0, True)

@pytest.mark.django_db
def test_message_when_leave_comment(rnd, p_1, p_2, move_factory):
    """make sure the right message appears if the user was not blocked"""
    move1 = move_factory(round=rnd, action_type=POST_SELFIE, player=p_1, victim=None)
    move2 = move_factory(round=rnd, action_type=LEAVE_COMMENT, player=p_2, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.post_selfie_msg(move1, 20, False, True)
    assert message(rnd.game, p_2.user.username) in message_service.leave_comment_msg(move2, p_1.user.username, 0, False)

@pytest.mark.django_db
def test_message_when_dislike(rnd, p_1, p_2, p_3, p_4, move_factory):
    """make sure the right message appears if the user was blocked"""
    move1 = move_factory(round=rnd, action_type=NO_MOVE, player=p_1, victim=None)
    move2 = move_factory(round=rnd, action_type=DISLIKE, player=p_2, victim=p_1)
    move3 = move_factory(round=rnd, action_type=DISLIKE, player=p_3, victim=p_1)
    move4 = move_factory(round=rnd, action_type=CALL_IPHONE, player=p_4, victim=p_3)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.no_move_msg(move1, NO_MOVE_DM, False)
    assert message(rnd.game, p_2.user.username) in message_service.dislike_msg(move2, p_1.user.username, 0, False)
    assert message(rnd.game, p_3.user.username) in message_service.dislike_msg(move3, p_1.user.username, 0, True)

@pytest.mark.django_db
def test_message_when_dislike_not_block(rnd, p_1, p_2, p_3, p_4, move_factory):
    """make sure the right message appears if the user was blocked"""
    move1 = move_factory(round=rnd, action_type=NO_MOVE, player=p_1, victim=None)
    move2 = move_factory(round=rnd, action_type=DISLIKE, player=p_2, victim=p_1)
    move3 = move_factory(round=rnd, action_type=DISLIKE, player=p_3, victim=p_1)
    tab = RoundTabulation(rnd).tabulate()
    assert message(rnd.game, p_1.user.username) in message_service.no_move_msg(move1, NO_MOVE_DM + (DISLIKE_DM * 2), True)
    assert message(rnd.game, p_2.user.username) in message_service.dislike_msg(move2, p_1.user.username, 0, False)
    assert message(rnd.game, p_3.user.username) in message_service.dislike_msg(move3, p_1.user.username, 0, False)
