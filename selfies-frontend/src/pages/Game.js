import React from 'react';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { wsConnect, wsDisconnect } from '../modules/websocket';
import {
  getGame, startRound, leaveGame, makeMove,
} from '../modules/game';
import withAuth from '../hocs/authWrapper';
import ChatBox from '../components/ChatBox';
import GameView from '../components/GameScreen';
import Navigation from '../components/Navigation';

class Game extends React.Component {
  componentDidMount() {
    const { id } = this.props;
    if (id) {
      this.connectAndJoin();
    }
  }

  connectAndJoin = async () => {
    const { id, dispatch } = this.props;
    const host = `ws://127.0.0.1:8000/ws/game/${id}?token=${localStorage.getItem('token')}`;
    await dispatch(wsConnect(host));
    dispatch(getGame(id));
  };

  leaveGame = async () => {
    const { id, dispatch, history } = this.props;
    const host = `ws://127.0.0.1:8000/ws/game/${id}?token=${localStorage.getItem('token')}`;
    await dispatch(leaveGame(id));
    await dispatch(wsDisconnect(host));
    history.push('/games');
  };

  startRound = () => {
    const { id, dispatch } = this.props;
    dispatch(startRound(id));
  };

  makeMove = () => {
    const { dispatch } = this.props;
    dispatch(makeMove('SELFIE'));
  };

  render() {
    const { id, game, time } = this.props;
    if (id) {
      return (
        <React.Fragment>
          <Navigation />
          <div style={{ display: 'flex', flexDirection: 'row' }}>
            <ChatBox game={game} />
            <div className="gamebox">
              <GameView game={game} />
              <div style={{ display: 'flex', flexDirection: 'row' }}>
                <button type="button" onClick={this.makeMove}>
                  post a selfie
                </button>
                <button type="button" onClick={this.leaveGame}>
                  leave game
                </button>
                <button type="button" onClick={this.startRound}>
                  start game
                </button>
                <span>{time}</span>
              </div>
            </div>
          </div>
        </React.Fragment>
      );
    }
    return `${<span> LOADING </span>}`;
  }
}

Game.propTypes = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  history: PropTypes.shape({
    push: PropTypes.func.isRequired,
  }).isRequired,
  game: PropTypes.shape({
    id: PropTypes.number,
    username: PropTypes.string,
  }),
  time: PropTypes.string,
};

Game.defaultProps = {
  id: PropTypes.string,
  dispatch: PropTypes.func,
  game: PropTypes.null,
  time: PropTypes.null,
};

const s2p = (state, ownProps) => ({
  id: ownProps.match && ownProps.match.params.id,
  username: state.auth.username,
  game: state.games.game,
  time: state.games.time,
});
export default withAuth(connect(s2p)(Game));
