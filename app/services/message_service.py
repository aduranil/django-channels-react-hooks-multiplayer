import random

from app.models import Message


def no_move_msg(move, comments=False):
    username = move.player.user.username
    message = "◆ {} was so lazy that she forgot to move 👀".format(username)
    message1 = "◆ {} was getting fillers so she forgot to move. I hope it was worth it! 💅".format(
        username
    )
    messages = [message, message1]
    if comments:
        message = "◆ {} didnt do anything, but she still got flamed 💅".format(username)
        message1 = "◆ {} got absolutely destroyed on social media for not posting this round. Her followers are finally done with her sorry ass! 💅".format(
            username
        )
        messages = [message]
    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=move.player.user.username,
        game=move.round.game,
    )
    return messages


def iphone_msg(move, victim, action_type):
    username = move.player.user.username

    message1 = "◆ {} tried to {}, but she was distracted by a phone call from {} 💅😂".format(
        victim, action_type, username
    )
    message2 = "◆ I feel bad for {} who tried to {} but couldn't because {} kept blowing up her phone! 💅😂".format(victim, action_type, username)

    messages = [message1, message2]
    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=move.player.user.username,
        game=move.round.game,
    )
    return messages


def go_live_message(move, followers, go_live_success, called):
    username = move.player.user.username
    if go_live_success:
        message1 = "◆ {} shared her political opinions while going live. chemtrails are real 👡👛".format(
            username
        )
        message2 = "◆ {} went live, but she just played old town road on repeat the whole time 📱".format(
            username
        )
        message3 = "◆ {} got shady during her go live sesh 📱".format(username)
        message4 = "◆ {} shared photos of her food while going live 📱".format(username)
        messages = [message1, message2, message3, message4]
    else:
        if not called:
            message1 = "◆ {} went live at the same time as other girls! how dumb was that? she lost {} followers 📱😩".format(
                username, followers
            )
            message2 = "◆ {} went live! she timed it poorly though and lost {} followers 📱😂".format(
                username, followers
            )
            messages = [message1, message2]
        else:
            message1 = "◆ {} tried to go live but she was called! 📱😩".format(
                username, followers
            )
            messages = [message1]

    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=move.player.user.username,
        game=move.round.game,
    )
    return messages


def leave_comment_msg(move, victim, grabbed=False):
    username = move.player.user.username
    message = "◆ {} decided to be petty and left a mean comment, ruining {}'s self esteem 🤳👎".format(
        username, victim
    )
    message2 = "◆ {} absolutely destroyed {}'s new selfie. She's a total hater 😮🤳😂!".format(
        username, victim
    )
    message3 = "◆ {} called {}'s bag cheap and tacky. What a mean comment 👛🤳".format(
        username, victim
    )
    messages = [message]
    if grabbed:
        message = "◆ {} tried to leave a mean comment for {}, but she was blocked! 📱🤳".format(
            username, victim
        )
        messages = [message]
    Message.objects.create(
        message=random.choice(messages),
        message_type="round_recap",
        username=username,
        game=move.round.game,
    )
    return messages


def dislike_msg(move, victim, points, grabbed, multiple_dislikes):
    username = move.player.user.username
    points = -points
    if multiple_dislikes:
        message = "◆ {} decided to dislike, ruining {}'s self esteem. 😈🤳".format(
            username, victim
        )
        messages = [message]
    else:
        message = "◆ {} tried to dislike {} all by herself, which did absolutely nothing 👡".format(
            username, victim
        )
        messages = [message]

    if grabbed:
        message1 = "◆ {} tried to dislike {}, but she was blocked! 🤳😩😩😩".format(
            username, victim
        )
        messages = [message1]
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
        message1 = "◆ If {} doesnt post again, she will be sorry 💋🤳".format(username)
        messages = [message1]

    else:
        message1 = "◆ {} didn't post. I dont know why since she had nothing better to do 💄".format(
            username
        )
        message2 = "◆ {} didn't have time to post for some reason. Doesn't she know the internet is more important than IRL?💄".format(
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
    message1 = "◆ {} posted a selfie. how original. Here are {} new followers🤳".format(
        username, followers
    )
    message2 = "◆ {} posted a selfie for {} new followers. cool i guess🤳👡".format(
        username, followers
    )
    message3 = "◆ {} delighted her {} followers with a beautiful selfie 👡".format(
        username, followers
    )
    message4 = "◆ {} posted a selfie for {} followers. I hope she got some views👡".format(
        username, followers
    )
    message5 = "◆ {} posted a selfie, like we really care what she's up to. She got {} followers for effort though".format(
        username, followers
    )
    message6 = "◆ {} tried to be part of a group selfie but no one wanted to join her. So its just her and the sad {} followers she gained".format(
        username, followers
    )
    message7 = "◆ {} took a group selfie with some other girls! But are they really friends? The extra popularity gained her {} followers".format(
        username, followers
    )
    message8 = "◆ {} somehow finagled her way into being part of a group selfie. The girls didn't care but she leeched off {} followers anyway".format(
        username, followers
    )
    messages = [
        message1,
        message2,
        message3,
        message4,
        message5,
        message6,
        message7,
        message8,
    ]
    if comments:
        message = "◆ {} got teased relentlessly for her ugly selfie. How cruel! She lost {} followers this round".format(
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
