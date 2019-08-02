import pytest

from .factories import RoundFactory
from app.models import Move, Round, GamePlayer

POST_SELFIE = "post_selfie"
POST_GROUP_SELFIE = "post_group_selfie"
POST_STORY = "post_story"
GO_LIVE = "go_live"
LEAVE_COMMENT = "leave_comment"
DONT_POST = "dont_post"
NO_MOVE = "no_move"


# @pytest.mark.django_db
# def test_dictionary_initialization(
#     game_factory,
#     user_factory,
#     game_player_factory,
#     round_factory,
#     move_factory
# ):
#     # make sure the dictionary of arrays with player ids by move is correct
#     game = game_factory()
#     round = round_factory(game=game, started=True)
#     users = [user_factory(), user_factory(), user_factory()]
#     gp = game_player_factory(game=game, user=users[0], started=True)
#     gp2 = game_player_factory(game=game, user=users[1], started=True)
#     gp3 = game_player_factory(game=game, user=users[2], started=True)
#     move_factory(round=round, action_type=Move.POST_SELFIE, player=gp)
#     move_factory(
#         round=round,
#         action_type=Move.LEAVE_COMMENT,
#         player=gp2,
#         victim=gp,
#     )
#     round_results = round.tabulate_round()
#     PLAYER_MOVES = dict([
#         (POST_SELFIE, [gp.user.id]),
#         (POST_GROUP_SELFIE, []),
#         (POST_STORY, []),
#         (GO_LIVE, []),
#         (LEAVE_COMMENT, [gp2.user.id]),
#         (DONT_POST, []),
#         (NO_MOVE, [gp3.user.id])]
#     )
#     assert round_results == PLAYER_MOVES


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
    move_factory(round=round, action_type=Move.POST_SELFIE, player=gp)
    move_factory(round=round, action_type=Move.LEAVE_COMMENT, player=gp2, victim=gp3)
    move_factory(round=round, action_type=Move.POST_GROUP_SELFIE, player=gp3)
    round_results = round.tabulate_round()
