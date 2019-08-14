import React, { useEffect } from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { wsConnect } from '../modules/websocket';
import WithAuth from '../hocs/AuthenticationWrapper';
import ChatBox from '../components/ChatBox';
import GameBox from '../components/GameBox';
import RoundHistory from '../components/RoundHistory';
import Navigation from '../components/Navigation';
import GameInfo from '../components/GameInfo';

const HOST = process.env.REACT_APP_WS_HOST;

function Game({
  id, time, dispatch, game, currentPlayer,
}) {
  const host = `ws://${HOST}/ws/game/${id}?token=${localStorage.getItem('token')}`;

  useEffect(() => dispatch(wsConnect(host)), [dispatch, host]);

  if (id && game) {
    return (
      <div
        style={{
          height: '100vh',
          maxHeight: '100vh',
          width: '100vw',
          display: 'flex',
          flexDirection: 'column',
        }}
      >
        <div>
          <Navigation inGame />
        </div>
        <div>
          <h1 style={{ textAlign: 'center', marginBottom: '5px' }}>{game.room_name}</h1>
        </div>
        <div style={{ display: 'flex', flexDirection: 'row', width: '100%' }}>
          <div className="game-card" style={{ maxHeight: '40vh' }}>
            <ChatBox game={game} />
          </div>
          <div className="game-card">
            <RoundHistory game={game} />
          </div>
        </div>
        <div style={{ display: 'flex', flexDirection: 'row', padding: '0.5%' }}>
          <GameInfo time={time} currentPlayer={currentPlayer} game={game} />
          <GameBox time={time} currentPlayer={currentPlayer} game={game} />
        </div>
      </div>
    );
  }
  return `${<span> LOADING </span>}`;
}

Game.propTypes = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  currentPlayer: PropTypes.shape({
    id: PropTypes.number.isRequired,
    followers: PropTypes.number.isRequired,
    stories: PropTypes.number.isRequired,
    username: PropTypes.string.isRequired,
    started: PropTypes.bool.isRequired,
  }),
  game: PropTypes.shape({
    id: PropTypes.number.isRequired,
    game_status: PropTypes.string.isRequired,
    is_joinable: PropTypes.bool.isRequired,
    room_name: PropTypes.string.isRequired,
    round_started: PropTypes.bool.isRequired,
    users: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        followers: PropTypes.number.isRequired,
        stories: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        started: PropTypes.bool.isRequired,
      }),
    ),
    messages: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
        message_type: PropTypes.string.isRequired,
        created_at: PropTypes.string.isRequired,
      }),
    ),
    round_history: PropTypes.arrayOf(
      PropTypes.shape({
        id: PropTypes.number.isRequired,
        username: PropTypes.string.isRequired,
        message: PropTypes.string.isRequired,
        message_type: PropTypes.string.isRequired,
        created_at: PropTypes.string.isRequired,
      }),
    ),
  }),
  time: PropTypes.string,
};

Game.defaultProps = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  game: PropTypes.null,
  time: PropTypes.null,
  currentPlayer: PropTypes.null,
};

const s2p = (state, ownProps) => ({
  id: ownProps.match && ownProps.match.params.id,
  username: state.auth.username,
  game: state.games.game,
  currentPlayer: state.games.currentPlayer,
  time: state.games.time,
});

export default WithAuth(connect(s2p)(Game));
