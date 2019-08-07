import pytest

from .factories import RoundFactory
from app.models import Move, Round, GamePlayer, Message

POST_SELFIE = "post_selfie"
POST_GROUP_SELFIE = "post_group_selfie"
POST_STORY = "post_story"
GO_LIVE = "go_live"
LEAVE_COMMENT = "leave_comment"
DONT_POST = "dont_post"
NO_MOVE = "no_move"
LEAVE_COMMENT_NO_MOVE = "leave_comment_no_move"
LEAVE_COMMENT_GROUP_SELFIE = "leave_comment_group_selfie"
GO_LIVE_DAMAGE = "go_live_damage"

POINTS = dict(
    [
        (POST_SELFIE, 10),
        (POST_GROUP_SELFIE, 20),
        (POST_STORY, 10),
        (GO_LIVE, 20),
        (LEAVE_COMMENT, -5),
        (LEAVE_COMMENT_NO_MOVE, -10),
        (LEAVE_COMMENT_GROUP_SELFIE, -15),
        (DONT_POST, 0),
        (NO_MOVE, -5),
        (GO_LIVE_DAMAGE, -15),
    ]
)


@pytest.mark.django_db
def test_when_one_player_goes_live(
    game_factory, user_factory, game_player_factory, round_factory, move_factory
):
    # make sure the dictionary of arrays with player ids by move is correct
    game = game_factory()
    round = round_factory(game=game, started=True)
    users = [user_factory(), user_factory(), user_factory()]
    gp = game_player_factory(game=game, user=users[0], started=True)
    gp2 = game_player_factory(game=game, user=users[1], started=True)
    gp3 = game_player_factory(game=game, user=users[2], started=True)
    move_factory(round=round, action_type=Move.GO_LIVE, player=gp)
    move_factory(round=round, action_type=Move.LEAVE_COMMENT, player=gp2, victim=gp3)
    move_factory(round=round, action_type=Move.POST_GROUP_SELFIE, player=gp3)
    round.tabulate_round()
    message = Message.objects.get(game=game, username=gp.user.username)
    assert (
        message.message
        == "{} went live and got {} followers. but for some reason she just played old town road on repeat the whole time".format(
            gp.user.username, POINTS[GO_LIVE]
        )
    )
    comment_message = Message.objects.get(game=game, username=gp2.user.username)
    assert (
        comment_message.message
        == "{} decided to be petty and left a mean comment, ruining {}'s self esteem".format(
            gp2.user.username, gp3.user.username
        )
    )
    group_selfie_message = Message.objects.get(game=game, username=gp3.user.username)
    assert (
        group_selfie_message.message
        == "{} got teased relentlessly for her ugly selfie. {} girls teased her. how cruel! she lost {} followers this round".format(
            gp3.user.username, 1, 20
        )
    )
