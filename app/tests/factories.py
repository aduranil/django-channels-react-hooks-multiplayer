import factory
from faker import Factory as FakerFactory

from django.contrib.auth.models import User
from django.utils.timezone import now

from app.models import Game, Message, GamePlayer, Round, Move

faker = FakerFactory.create()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Faker("safe_email")
    username = factory.LazyAttribute(lambda x: faker.name())

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(UserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user


class GameFactory(factory.django.DjangoModelFactory):
    room_name = factory.LazyAttribute(lambda x: faker.name())
    game_status = "active"
    created_at = factory.LazyAttribute(lambda x: now())
    updated_at = factory.LazyAttribute(lambda x: now())
    round_started = False
    is_joinable = True

    class Meta:
        model = Game


class GamePlayerFactory(factory.django.DjangoModelFactory):
    followers = 0
    stories = 3
    user = factory.SubFactory(UserFactory)
    started = False
    game = factory.SubFactory(GameFactory)

    class Meta:
        model = GamePlayer


class MessageFactory(factory.django.DjangoModelFactory):
    game = factory.SubFactory(GameFactory)
    username = None
    message = factory.LazyAttribute(lambda x: faker.sentence())
    created_at = factory.LazyAttribute(lambda x: now())
    message_type = None

    class Meta:
        model = Message


class RoundFactory(factory.django.DjangoModelFactory):
    game = factory.SubFactory(GameFactory)
    started = False

    class Meta:
        model = Round


class MoveFactory(factory.django.DjangoModelFactory):
    round = factory.SubFactory(RoundFactory)
    action_type = "dont_post"
    player = factory.SubFactory(GamePlayerFactory)
    victim = factory.SubFactory(GamePlayerFactory)

    class Meta:
        model = Move
