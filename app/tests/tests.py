import pytest


@pytest.mark.django_db
def test_can_start_game(setup_3player_game):
    assert setup_3player_game.can_start_game() is False
