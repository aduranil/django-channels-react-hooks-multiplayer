import random

from app.models import Message


def no_move_msg(move, followers, comments=False):
    username = move.player.user.username
    message = "{} was so lazy that she forgot to move. she lost {} followers".format(
        username, followers
    )
    messages = [message]
    if comments:
        message = "{} didnt do anything, but she still got flamed and lost {} followers".format(
            username, followers
        )
        messages = [message]
    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=move.player.user.username,
        game=move.round.game,
    )
    return messages

def iphone_msg(move, victim):
    username = move.player.user.username
    message1 = "{} tried to go live, but she was distracted by a phone call from {}".format(
        victim, username
    )
    messages = [message1]
    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=move.player.user.username,
        game=move.round.game,
    )
    return messages


def leave_comment_msg(move, victim, points, grabbed=False):
    username = move.player.user.username
    message = "{} decided to be petty and left a mean comment, ruining {}'s self esteem. she got {} followers this round".format(
        username, victim, points
    )
    messages = [message]
    if grabbed:
        message = "{} tried to leave a mean comment for {}, but she was blocked! she got {} followers this round".format(
            username, victim, points
        )
        messages = [message]
    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=username,
        game=move.round.game,
    )
    return messages

def dont_post_msg(move, repeat=False):
    username = move.player.user.username
    messages = []
    if repeat:
        message1 = "if {} doesnt post again, she will be sorry".format(username)
        messages = [message1]

    else:
        message1 = "{} didn't post. i dont know why since she had nothing better to do".format(
            username
        )
        message2 = "{} didn't have time to post for some reason. doesn't she know the internet is more important than IRL?".format(
            username
        )
        messages = [message1, message2]
    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=move.player.user.username,
        game=move.round.game,
    )
    return messages


def post_selfie_msg(move, followers, called=False, comments=False):
    username = move.player.user.username
    message1 = "{} posted a selfie. how original. here are {} new followers".format(username, followers)
    message2 = "{} posted a selfie for {} new followers. cool i guess".format(username, followers)
    message3 = "{} delighted her {} new followers with a beautiful selfie".format(username, followers)
    message4 = "{} posted a selfie for {} followers. i hope she got some views".format(
        username, followers
    )
    message5 = "{} posted a selfie, like we really care what she's up to. she got {} followers for effort though".format(
        username, followers
    )
    message6 = "{} tried to be part of a group selfie but no one wanted to join her. so its just her and the sad {} followers she gained".format(
        username, followers
    )
    message7 = "{} took a group selfie with some other girls! but are they really friends? the extra popularity gained her {} followers".format(
        username, followers
    )
    message8 = "{} somehow finagled her way into being part of a group selfie. the girls didn't care but she leeched off {} followers anyway".format(
        username, followers
    )
    messages = [message1, message2, message3, message4, message5, message6, message7, message8]
    if comments:
        message = "{} got teased relentlessly for her ugly selfie. how cruel! she lost {} followers this round".format(
            username, followers
        )
        messages = [message]

    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=move.player.user.username,
        game=move.round.game,
    )
    return messages
