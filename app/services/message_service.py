import random

from app.models import Message


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


def post_selfie_msg(move, called=False, comments=False):
    username = move.player.user.username
    message1 = "{} posted a selfie. how original".format(username)
    message2 = "{} posted a selfie. cool i guess".format(username)
    message3 = "{} delighted her followers with a beautiful selfie".format(username)
    messages = [message1, message2, message3]
    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=move.player.user.username,
        game=move.round.game,
    )
    return messages
