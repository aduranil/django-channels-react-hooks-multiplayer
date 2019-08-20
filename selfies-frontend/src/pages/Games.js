import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import Navigation from '../components/Navigation';
import { createGame, getGames } from '../modules/game';
import WithAuth from '../hocs/AuthenticationWrapper';
import HalfRectangle from '../images/Rectangle';

function Games({
  history, dispatch, loggedIn, games,
}) {
  const [roomName, setRoomName] = useState('');

  useEffect(
    () => {
      if (loggedIn) {
        dispatch(getGames());
      }
    },
    [dispatch, loggedIn],
  );

  const onClick = () => {
    if (roomName.length === 0) {
      return alert('You must include a room name');
    }
    return dispatch(createGame(roomName)).then((data) => {
      history.push(data);
    });
  };

  const onJoin = async (e) => {
    await history.push(`/game/${e.target.value}`);
  };

  return (
    <React.Fragment>
      <HalfRectangle color="#70D6FF" />
      <Navigation />
      <h1 style={{ textAlign: 'center' }}>Active Games</h1>
      <div className="landingbox">
        <div style={{ display: 'flex' }}>
          <button type="button" style={{ marginRight: '10px' }} onClick={onClick}>
            create game
          </button>
          <input
            value={roomName}
            onChange={event => setRoomName(event.target.value)}
            placeholder="room name"
            onKeyPress={e => e.key === 'Enter' && onClick()}
            style={{ flexGrow: '1' }}
          />
        </div>
        <div
          style={{
            overflowY: 'scroll',
            height: '50vh',
            maxHeight: '60vh',
          }}
        >
          {Array.isArray(games.games)
            && games.games.map(game => (
              <div
                style={{
                  marginTop: '10px',
                  marginBottom: '5px',
                }}
                key={game.id}
              >
                <button
                  type="button"
                  onClick={onJoin}
                  style={{ marginRight: '10px' }}
                  value={game.id}
                  disabled={game.is_joinable === false}
                >
                  join
                </button>
                <span>
                  {game.room_name}
                  , players:
                  {' '}
                </span>
                {game.users.map(user => (
                  <span key={user.username}>
                    {' '}
                    {user.username}
                    ,
                  </span>
                ))}
              </div>
            ))}
        </div>
      </div>
    </React.Fragment>
  );
}

const s2p = state => ({
  games: state.games,
  loggedIn: state.auth.loggedIn,
});

Games.propTypes = {
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  dispatch: PropTypes.func,
  games: PropTypes.shape({
    id: PropTypes.number,
    game_status: PropTypes.string,
    room_name: PropTypes.string,
    users: PropTypes.shape({
      id: PropTypes.number,
      username: PropTypes.string,
    }),
  }),
  loggedIn: PropTypes.bool,
};

Games.defaultProps = {
  dispatch: PropTypes.func,
  games: PropTypes.null,
  loggedIn: PropTypes.bool,
};

export default WithAuth(connect(s2p)(Games));
