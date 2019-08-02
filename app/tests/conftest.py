import pytest
from pytest_factoryboy import register

from .factories import (
    UserFactory,
    GameFactory,
    GamePlayerFactory,
    MoveFactory,
    RoundFactory,
)

register(UserFactory)
register(GameFactory)
register(GamePlayerFactory)
register(MoveFactory)
register(RoundFactory)
