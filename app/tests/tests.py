import pytest

from app.models import Move, Round, GamePlayer, Message, POINTS

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
LEAVE_COMMENT_SELF_POINTS = "leave_comment_self_points"

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

def post_selfie(username, followers):
    message1 = "{} posted a selfie. how original. she gained {} followers".format(
        username, followers
    )
    message2 = "{} posted a selfie. cool i guess. she got {} followers".format(
        username, followers
    )
    message3 = "{} delighted her followers with a beautiful selfie and gained {} followers".format(
        username, followers
    )
    return [message1, message2, message3]

def go_live(username, followers):
    message = "{} went live and got {} followers. but for some reason she just played old town road on repeat the whole time".format(username, followers)
    return [message]

def many_went_live(username, followers):
    message = "{} went live at the same time as other girls! how dumb was that? she lost {} followers".format(username, followers)
    return [message]

def dont_post(username, followers):
    message1 = "{} didn't post and lost {} followers. i dont know why since she had nothing better to do".format(
        username, followers
    )
    message2 = "{} didn't have time to post for some reason. doesn't she know the internet is more important than IRL? she lost {} followers".format(
        username, followers
    )
    return [message1, message2]

def no_move(username, followers):
    message = "{} was so lazy that she forgot to move. she lost {} followers".format(
        username, followers
    )
    return [message]

def post_group_selfie(username, followers):
    message1 = "{} took a group selfie with some other girls! but are they really friends? the extra popularity gained her {} followers".format(
        username, followers
    )
    message2 = "{} somehow finagled her way into being part of a group selfie. the girls didn't care but she leeched off {} followers anyway".format(
        username, followers
    )
    return [message1, message2]

def post_story(username, followers):
    message1 = "{} posted a story for {} followers. i hope she got some views".format(
        username, followers
    )
    message2 = "{} posted a story, like we really care what she's up to. she got {} followers for effort though".format(
        username, followers
    )
    return [message1, message2]

def leave_comment(username, extra):
    message = "{} decided to be petty and left a mean comment, ruining {}'s self esteem".format(
        username, extra
    )
    return [message]

def one_group_selfie(username, followers):
    message = "{} tried to be part of a group selfie but no one wanted to join her. so its just her and the sad {} followers she gained".format(
        username, followers
    )
    return [message]

def go_live_damage(username, followers, extra):
    message = "{} tried to get attention but {} was live, capturing her followers attention. {} lost {} followers".format(
        username, extra, username, followers
    )
    return [message]

def many_went_live(username, followers):
    message = "{} went live at the same time as other girls! how dumb was that? she lost {} followers".format(username, followers)
    return [message]

def selfie_victim(username, followers, extra):
    message = "{} got teased relentlessly for her ugly selfie. {} girls teased her. how cruel! she lost {} followers this round".format(
        username, extra, followers
    )
    return [message]

def no_move_victim(username, followers):
    message = "{} didnt do anythng, but she still got flamed and lost {} followers".format(
        username, followers)
    return [message]

def message(game, username):
    return Message.objects.get(game=game, username=username).message

@pytest.mark.django_db
def test_when_one_player_goes_live(game, rnd, p_1, p_2, p_3, move_factory):
    # make sure the dictionary of arrays with player ids by move is correct
    move_factory(round=rnd, action_type=Move.GO_LIVE, player=p_1)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_2, victim=p_3)
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_3)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in go_live(p_1.user.username, POINTS[GO_LIVE])
    assert round[p_1.id] == 20

    assert message(game=game, username=p_2.user.username) in leave_comment(p_2.user.username, p_3.user.username)
    assert round[p_2.id] == 0

    assert message(game=game, username=p_3.user.username) in selfie_victim(p_3.user.username, 20, 1)
    # lost 15 points for taking a selfie during a go_live, and 5 points for getting teased
    assert round[p_3.id] == -20

@pytest.mark.django_db
def test_when_two_players_go_live(game, rnd, p_1, p_2, p_3, move_factory):
    # make sure the dictionary of arrays with player ids by move is correct
    move_factory(round=rnd, action_type=Move.GO_LIVE, player=p_1)
    move_factory(round=rnd, action_type=Move.GO_LIVE, player=p_2)
    move_factory(round=rnd, action_type=Move.POST_SELFIE, player=p_3)
    round = rnd.tabulate_round()

    message = Message.objects.get(game=game, username=p_1.user.username)
    assert message.message in many_went_live(p_1.user.username, 20)
    assert round[p_1.id] == -20

    message_two = Message.objects.get(game=game, username=p_2.user.username)
    assert message_two.message in many_went_live(p_2.user.username, 20)
    assert round[p_2.id] == -20

    post_selfie_message = Message.objects.get(game=game, username=p_3.user.username)
    assert post_selfie_message.message in post_selfie(p_3.user.username, 10)
    assert round[p_3.id] == 10

@pytest.mark.django_db
def test_no_move_and_story(game, rnd, p_1, p_2, p_3, move_factory):
    # make sure the dictionary of arrays with player ids by move is correct

    move_factory(round=rnd, action_type=Move.POST_STORY, player=p_3)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in no_move(p_1.user.username, 5)
    assert round[p_1.id] == -5

    assert message(game=game, username=p_2.user.username) in no_move(p_2.user.username, 5)
    assert round[p_2.id] == -5

    assert message(game=game, username=p_3.user.username) in post_story(p_3.user.username, 10)
    assert round[p_3.id] == 10

@pytest.mark.django_db
def test_group_selfie_everyone(game, rnd, p_1, p_2, p_3, move_factory):
    # make sure the dictionary of arrays with player ids by move is correct
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_1)
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_2)
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_3)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in post_group_selfie(p_1.user.username, 20)
    assert round[p_1.id] == 20

    assert message(game=game, username=p_2.user.username) in post_group_selfie(p_2.user.username, 20)
    assert round[p_2.id] == 20

    assert message(game=game, username=p_3.user.username) in post_group_selfie(p_3.user.username, 20)
    assert round[p_3.id] == 20

@pytest.mark.django_db
def test_group_selfie_selfies_story(game, rnd, p_1, p_2, p_3, move_factory):
    # make sure the dictionary of arrays with player ids by move is correct
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_1)
    move_factory(round=rnd, action_type=Move.POST_SELFIE, player=p_2)
    move_factory(round=rnd, action_type=Move.POST_STORY, player=p_3)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in one_group_selfie(p_1.user.username, 10)
    assert round[p_1.id] == 10

    assert message(game=game, username=p_2.user.username) in post_selfie(p_2.user.username, 10)
    assert round[p_2.id] == 10

    assert message(game=game, username=p_3.user.username) in post_story(p_3.user.username, 10)
    assert round[p_3.id] == 10

@pytest.mark.django_db
def test_leave_comment_group_selfie(game, rnd, p_1, p_2, p_3, move_factory):
    # make sure the dictionary of arrays with player ids by move is correct
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_1)
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_2)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_3, victim=p_2)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in post_group_selfie(p_1.user.username, 20)
    assert round[p_1.id] == 20

    assert message(game=game, username=p_2.user.username) in selfie_victim(p_2.user.username, 15, 1)
    assert round[p_2.id] == -15

    assert message(game=game, username=p_3.user.username) in leave_comment(p_3.user.username, p_2.user.username)
    assert round[p_3.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

@pytest.mark.django_db
def test_leave_comment_group_selfie_go_live(game, rnd, p_1, p_2, p_3, p_4, move_factory):
    # make sure the dictionary of arrays with player ids by move is correct
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_1)
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_2)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_3, victim=p_2)
    move_factory(round=rnd, action_type=Move.GO_LIVE, player=p_4)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in go_live_damage(p_1.user.username, -POINTS[GO_LIVE_DAMAGE], p_4.user.username)
    assert round[p_1.id] == POINTS[GO_LIVE_DAMAGE]

    total_points = POINTS[LEAVE_COMMENT_GROUP_SELFIE] + POINTS[GO_LIVE_DAMAGE]
    assert message(game=game, username=p_2.user.username) in selfie_victim(p_2.user.username, -total_points, 1)
    assert round[p_2.id] == total_points

    assert message(game=game, username=p_3.user.username) in leave_comment(p_3.user.username, p_2.user.username)
    assert round[p_3.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_4.user.username) in go_live(p_4.user.username, POINTS[GO_LIVE])
    assert round[p_4.id] == POINTS[GO_LIVE]

@pytest.mark.django_db
def test_leave_comment_group_selfie_two_go_live(game, rnd, p_1, p_2, p_3, p_4, p_5, move_factory):
    # make sure the dictionary of arrays with player ids by move is correct
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_1)
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_2)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_3, victim=p_2)
    move_factory(round=rnd, action_type=Move.GO_LIVE, player=p_4)
    move_factory(round=rnd, action_type=Move.GO_LIVE, player=p_5)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in post_group_selfie(p_1.user.username, POINTS[POST_GROUP_SELFIE])
    assert round[p_1.id] == POINTS[POST_GROUP_SELFIE]

    assert message(game=game, username=p_2.user.username) in selfie_victim(p_2.user.username, -POINTS[LEAVE_COMMENT_GROUP_SELFIE], 1)
    assert round[p_2.id] == POINTS[LEAVE_COMMENT_GROUP_SELFIE]

    assert message(game=game, username=p_3.user.username) in leave_comment(p_3.user.username, p_2.user.username)
    assert round[p_3.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_4.user.username) in many_went_live(p_4.user.username, POINTS[GO_LIVE])
    assert round[p_4.id] == -POINTS[GO_LIVE]

    assert message(game=game, username=p_5.user.username) in many_went_live(p_5.user.username, POINTS[GO_LIVE])
    assert round[p_5.id] == -POINTS[GO_LIVE]

@pytest.mark.django_db
def test_2leave_comment_group_selfie_go_live(game, rnd, p_1, p_2, p_3, p_4, p_5, p_6,move_factory):
    # make sure the dictionary of arrays with player ids by move is correct
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_1)
    move_factory(round=rnd, action_type=Move.POST_GROUP_SELFIE, player=p_2)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_3, victim=p_2)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_6, victim=p_2)
    move_factory(round=rnd, action_type=Move.GO_LIVE, player=p_4)
    move_factory(round=rnd, action_type=Move.DONT_POST, player=p_5)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in go_live_damage(p_1.user.username, -POINTS[GO_LIVE_DAMAGE], p_4.user.username)
    assert round[p_1.id] == POINTS[GO_LIVE_DAMAGE]

    total_points = (POINTS[LEAVE_COMMENT_GROUP_SELFIE] * 2) + POINTS[GO_LIVE_DAMAGE]
    assert message(game=game, username=p_2.user.username) in selfie_victim(p_2.user.username, -total_points, 2)
    assert round[p_2.id] == total_points

    assert message(game=game, username=p_3.user.username) in leave_comment(p_3.user.username, p_2.user.username)
    assert round[p_3.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_6.user.username) in leave_comment(p_6.user.username, p_2.user.username)
    assert round[p_6.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_4.user.username) in go_live(p_4.user.username, POINTS[GO_LIVE])
    assert round[p_4.id] == POINTS[GO_LIVE]

    assert message(game=game, username=p_5.user.username) in dont_post(p_5.user.username, POINTS[DONT_POST])
    assert round[p_5.id] == POINTS[DONT_POST]

@pytest.mark.django_db
def test_everyone_leaves_a_mean_comment(game, rnd, p_1, p_2, p_3, p_4, p_5, p_6,move_factory):
    # make sure the dictionary of arrays with player ids by move is correct

    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_1, victim=p_2)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_2, victim=p_1)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_3, victim=p_3)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_4, victim=p_5)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_5, victim=p_6)
    move_factory(round=rnd, action_type=Move.LEAVE_COMMENT, player=p_6, victim=p_5)
    round = rnd.tabulate_round()

    assert message(game=game, username=p_1.user.username) in leave_comment(p_1.user.username, p_2.user.username)
    assert round[p_1.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_2.user.username) in leave_comment(p_2.user.username, p_1.user.username)
    assert round[p_2.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_3.user.username) in leave_comment(p_3.user.username, p_3.user.username)
    assert round[p_3.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_4.user.username) in leave_comment(p_4.user.username, p_5.user.username)
    assert round[p_4.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_5.user.username) in leave_comment(p_5.user.username, p_6.user.username)
    assert round[p_5.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]

    assert message(game=game, username=p_6.user.username) in leave_comment(p_6.user.username, p_5.user.username)
    assert round[p_6.id] == POINTS[LEAVE_COMMENT_SELF_POINTS]
